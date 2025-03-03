# Changelog — latex2pydata Python package


## v0.5.0 (dev)

*  Renamed schema missing setting `rawstr` to `verbatim`.

*  Added schema support for `Any` type.  Added schema support for `verbatim`
   type, which keeps the string value received from LaTeX without any
   interpretation.

*  Improved schema documentation.



## v0.4.1 (2024-11-24)

*  `pyproject.toml`:  explicitly set `build-backend` (#1).



## v0.4.0 (2024-06-04)

*  Replaced type definitions with type annotations for compatibility with
   Python 3.8.  Switched back to v0.2.0 type annotations, since they
   require no modification with `from __future__ import annotations`.


## v0.3.0 (2024-06-03)

*  Modified type hints for compatibility with Python >= 3.9.  Previously used
   Python 3.10 notation for Union and Optional types.  Modified
   `requires-python` in `pyproject.toml` accordingly.


## v0.2.0 (2024-05-16)

*  `load()` and `loads()` now take optional `schema` and `schema_missing`
   arguments.  These override any schema settings in the file/string metadata.


## v0.1.0 (2023-11-20)

*  Initial release.
