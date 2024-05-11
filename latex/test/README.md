# Test `latex2pydata`

This directory contains several `.tex` documents for testing the
`latex2pydata` package.

Documents with names ending in `_fail` should cause LaTeX to exit with a
nonzero exit code.

Documents with names ending in `_pass` should compile successfully with LaTeX.
During compilation, these documents will create one or more `.pydata` files.
For these documents, there are also `.json` files containing the expected data
and/or `.testdata` files containing the expected literal content of the
`.pydata` files.  Loading the `.pydata` files to obtain a successful data
match with the `.json` files requires that the
[`latex2pydata` Python package](https://github.com/gpoore/latex2pydata/tree/main/python)
be installed in some cases.

To run tests, simply execute the include Python script `test_latex2pydata.py`.
This will run all tests if the `latex2pydata` Python package is installed.
Otherwise it will issue a warning and run all tests that do not rely on the
Python package.
