# `latex2pydata` - write data to file in Python literal format

`latex2pydata` is a [LaTeX](https://www.latex-project.org/) package for
writing data to file using
[Python literal syntax](https://docs.python.org/3/reference/lexical_analysis.html#literals).
The data may be loaded safely in Python using the
[`ast.literal_eval()`](https://docs.python.org/3/library/ast.html#ast.literal_eval)
function or the
[`latex2pydata` Python package](https://github.com/gpoore/latex2pydata_py).

The top-level data structure can be configured as either a Python dict or a
list of dicts.  Within dicts, all keys and values are written to file as
Python string literals.  However, this does not limit the data types that can
be passed from LaTeX to Python.  When data is loaded, the included schema
functionality makes it possible to convert string values into other Python
data types such as dicts, lists, sets, bools, and numbers.

The data is suitable for direct loading in Python with `ast.literal_eval()`.
It is also possible to load data using the
[`latex2pydata` Python package](https://github.com/gpoore/latex2pydata_py).
This functions as a wrapper for `ast.literal_eval()`.  The package requires
all keys to match the regex `[A-Za-z_][0-9A-Za-z_]*`.  Periods in keys are
interpreted as key paths and indicate sub-dicts.  For example, the key path
`main.sub` represents a key `main` in the main dict that maps to a sub-dict
containing a key `sub`.  The Python package supports the schema features
provided by the LaTeX package, so that data types other than dicts of strings
are possible.


## Installation

The easiest option with an up-to-date LaTeX distribution like
[TeX Live](https://tug.org/texlive/) or [MiKTeX](https://miktex.org/)
is to use the package manager.  Depending on how LaTeX is configured,
you may already have `latex2pydata` installed, and can update it
with the package manager if necessary.

To try the development version, simply download `latex2pydata.sty` and put it
in the same directory as your document.

There are many resources online for manual package installation. The
[LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX/Installing_Extra_Packages#Manual_installation)
might be one place to start.  Note that for manual installation, the style
file `latex2pydata.sty` is pre-generated and available for download.


## License

This work may be distributed and/or modified under the conditions of the
[LaTeX Project Public License](http://www.latex-project.org/lppl.txt) (LPPL),
version 1.3c or later.
