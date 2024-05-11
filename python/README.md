# latex2pydata - load data from LaTeX in Python literal format

The latex2pydata Python package is designed to load data in
[Python literal format](https://docs.python.org/3/reference/lexical_analysis.html#literals)
that was saved to file by the
[latex2pydata LaTeX package](https://github.com/gpoore/latex2pydata_tex).
This allows data to be passed from [LaTeX](https://www.latex-project.org/) to
Python.

Raw data is loaded with
[`ast.literal_eval()`](https://docs.python.org/3/library/ast.html#ast.literal_eval).  This always yields either `dict[str,str]` or
`list[dict[str,str]]`.  Then data is postprocessed to apply any schemas and to unpack key paths.

* The LaTeX package allows schemas to be defined using Python type annotation
  syntax.  When a schema exists, string values are evaluated with
  `ast.literal_eval()`, and then the data type of each result is checked
  against the schema.

* All dict keys are required to match the regex `[A-Za-z_][0-9A-Za-z_]*`.
  Periods in keys are interpreted as key paths and indicate sub-dicts.  For
  example, the key path `main.sub` represents a key `main` in the main dict
  that maps to a sub-dict containing a key `sub`.


## Schema support

The current parser for Python type annotation syntax is basic and limits the
supported schema data types:

* Nested collection data types are only supported 2 levels deep.  So
  `list[list[int]]` is fine, but `list[list[list[int]]]` is not supported.

* Collection union types are not supported.  For example, `set[int]|list[int]`
  is not supported.  (Scalar union types such as `float|int` are supported.)

It is possible to work around these limitations by setting
`\pydatasetschemamissing{evalany}` on the LaTeX side.  This causes all values
without a schema definition to be evaluated with `ast.literal_eval()`, and
skips type checking for values that are not defined in the schema.

Currently, if a key path is used in defining a schema value or setting a
data value, then the same key path must be used in both the schema and the
data.  That is, schema validation is currently performed before key path
unpacking.

See the source code and the
[latex2pydata LaTeX package](https://github.com/gpoore/latex2pydata_tex)
documentation for additional details about schema support.


## Keys and key paths

Data is interpreted as Python literals.  Thus, there is no checking for
duplicate keys.  If a key is defined multiple times, later values replace
earlier values.  Similarly, there is no checking for duplicate keys during
key path unpacking.


## Usage

The package provides two functions for loading data:
* `load(<filehandle or pathlib.Path>, encoding='utf-8-sig')`
* `loads(<string>)`


## Tests

The latex2pydata Python package includes tests.  Additional tests are part
of the
[latex2pydata LaTeX package](https://github.com/gpoore/latex2pydata_tex).
