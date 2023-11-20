import ast
import hashlib
import json
import os
import pathlib
import subprocess
import shutil
import sys
import textwrap

try:
    import latex2pydata
except ImportError:
    latex2pydata = None


if not pathlib.Path.cwd().parts[-2:] == ('latex2pydata_tex', 'test'):
    sys.exit('Tests must run with latex2pydata_tex/test/ as the working directory')

texfiles_tested: set[pathlib.Path] = set()
test_failures: list[str] = []
texfiles_failed: set[pathlib.Path] = set()
test_dir = pathlib.Path.cwd()
latex_dir = test_dir.parent / 'latex2pydata'

termcolors: dict[str, int] = {
    'red': 31,
    'green': 32,
    'yellow': 33,
}
def print_color(string, color=None,  end='\n', flush=False):
    if color is None or not sys.stdout.isatty():
        print(string, end=end, flush=flush)
        return
    color_num = termcolors[color]
    print(f'\x1b[{color_num}m{string}\x1b[39m', end=end, flush=flush)
def print_progress_color(string=None, color=None, clear=False, end='\n', flush=False):
    if string is None and not clear:
        raise TypeError
    if clear:
        print('\x1b[2K\r', end='')
    if string is not None:
        print_color(string, color=color, end=end, flush=flush)


# update latex2pydata.sty in test dir
os.chdir(latex_dir)
try:
    subprocess.run(['latex', 'latex2pydata.ins'], check=True, capture_output=True)
except subprocess.CalledProcessError as e:
    sys.exit(f'Failed to generate "latex2pydata.sty":\n{e}')
shutil.copy(latex_dir / 'latex2pydata.sty', test_dir)
os.chdir(test_dir)

if latex2pydata is None:
    print_color('Warning:  Could not import latex2pydata, so schema tests will be skipped', 'yellow')

if len(sys.argv) == 1:
    texfiles = list(pathlib.Path().glob('*.tex'))
else:
    texfiles = [pathlib.Path(x) for x in sys.argv[1:]]
for n, texfile in enumerate(texfiles):
    texfiles_tested.add(texfile)
    print_progress_color(f'\rlatex2pydata test {n: >2}/{len(texfiles)}', end='')
    expected_status = texfile.stem.rsplit('_', 1)[-1]
    if expected_status not in ('pass', 'fail'):
        texfiles_failed.add(texfile)
        test_failures.append(f'Test "{texfile}" does not have name ending in "_pass" or "_fail"')
        continue
    pydata = texfile.parent / f'{texfile.stem}.pydata'
    test_data = texfile.parent / f'{texfile.stem}.testdata'
    test_json = texfile.parent / f'{texfile.stem}.json'
    pdf = texfile.parent / f'{texfile.stem}.pdf'
    cleanup = [texfile.parent / f'{texfile.stem}.{ext}' for ext in ('aux', 'log', 'synctex.gz', 'fdb_latexmk', 'fls')]
    if expected_status == 'pass' and not (test_data.is_file() or test_json.is_file()):
        texfiles_failed.add(texfile)
        test_failures.append(f'Test "{texfile}" is missing a data comparison file "{test_data}" or "{test_json}"')
        continue
    for latex in ('pdflatex', 'xelatex', 'lualatex'):
        pydata.unlink(missing_ok=True)
        for tempfile in cleanup:
            tempfile.unlink(missing_ok=True)
        try:
            subprocess.run(
                [latex, '-interaction=nonstopmode', texfile.as_posix()],
                check=True, capture_output=True,
                encoding='utf8', errors='backslashreplace',
            )
        except subprocess.CalledProcessError as e:
            if expected_status == 'pass':
                texfiles_failed.add(texfile)
                test_failures.append(f'Test "{texfile}" failed to compile successfully ({latex}):\n{e.output}')
                break
            continue
        if expected_status == 'fail':
            texfiles_failed.add(texfile)
            test_failures.append(f'Test "{texfile}" should have failed but compiled successfully ({latex})')
            break
        if not pydata.is_file():
            texfiles_failed.add(texfile)
            test_failures.append(f'Test "{texfile}" failed to create a data file "{pydata}" ({latex})')
            break
        if test_data.is_file():
            if pydata.read_text(encoding='utf8') != test_data.read_text(encoding='utf8'):
                texfiles_failed.add(texfile)
                test_failures.append(
                    f'Test "{texfile}" created data "{pydata}" that does not match "{test_data}" ({latex})'
                )
                break
        if test_json.is_file():
            try:
                if 'schema' in texfile.name:
                    if latex2pydata is None:
                        # It would be possible to skip over the schema files
                        # before running LaTeX, but that would miss the
                        # opportunity to check for other errors
                        texfiles_tested.remove(texfile)
                        break
                    loaded_pydata = latex2pydata.load(pydata)
                else:
                    loaded_pydata = ast.literal_eval(pydata.read_text(encoding='utf8'))
            except Exception as e:
                texfiles_failed.add(texfile)
                test_failures.append(f'Test "{texfile}" created data "{pydata}" that failed to load ({latex}):\n{e}')
                break
            try:
                loaded_json = json.loads(test_json.read_bytes())
            except Exception as e:
                texfiles_failed.add(texfile)
                test_failures.append(f'JSON test data "{test_json}" is invalid:\n{e}')
                break
            if isinstance(loaded_pydata, dict) and 'buffermd5' in loaded_pydata and 'buffermd5' not in loaded_json:
                hasher = hashlib.md5()
                for line in pydata.read_text(encoding='utf8').splitlines():
                    if line.lstrip().startswith(('{', '}', '[', ']')):
                        continue
                    if line.lstrip().startswith('"buffermd5"'):
                        break
                    hasher.update(f'{line}\n'.encode('utf8'))
                loaded_json['buffermd5'] = hasher.hexdigest().upper()
            if loaded_pydata != loaded_json:
                texfiles_failed.add(texfile)
                test_failures.append(
                    f'Test "{texfile}" created data "{pydata}" that failed comparison with "{test_json}"'
                )
                break
    if texfile not in texfiles_failed:
        pydata.unlink(missing_ok=True)
        pdf.unlink(missing_ok=True)
    for tempfile in cleanup:
        tempfile.unlink(missing_ok=True)
print_progress_color(clear=True)

if not texfiles_failed:
    if len(texfiles) == len(texfiles_tested):
        print_color(f'Passed all {len(texfiles_tested)} tests!', 'green')
    else:
        print_color(f'Passed {len(texfiles_tested)} tests!', 'green', end='')
        print('  ', end='')
        skipped = len(texfiles) - len(texfiles_tested)
        print_color(f'[Skipped {skipped} test(s); missing latex2pydata Python package.]', 'yellow')
    sys.exit(0)
print_color(f'Failed {len(test_failures)}/{len(texfiles_tested)} tests.  Errors:', 'red')
if sys.stdout.isatty():
    width = shutil.get_terminal_size()[0]
else:
    width = 80
for failure in test_failures:
    for n, line in enumerate(failure.splitlines()):
        if n == 0:
            print()
        if len(line) < width - 2:
            if n == 0:
                print_color(f'* {line}', 'red')
            else:
                print(f'  {line}')
        elif n == 0:
            print_color(textwrap.fill(line, width=width, initial_indent='* ', subsequent_indent='  '), 'red')
        else:
            print(textwrap.fill(line, width=width, initial_indent='  ', subsequent_indent='  '))
print()
print_color(f'Failed {len(texfiles_failed)}/{len(texfiles_tested)} tests', 'red')
sys.exit(1)
