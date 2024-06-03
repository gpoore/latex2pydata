# Changelog — latex2pydata Python package


## v0.3.0 (2024-06-03)

*  Modified type hints for compatibility with Python >= 3.9.  Previously used
   Python 3.10 notation for Union and Optional types.  Modified
   `requires-python` in `pyproject.toml` accordingly.


## v0.2.0 (2024-05-16)

*  `load()` and `loads()` now take optional `schema` and `schema_missing`
   arguments.  These override any schema settings in the file/string metadata.


## v0.1.0 (2023-11-20)

*  Initial release.
