# Changelog


## v0.2.0 (dev)

*  Bools for tracking state are now global.  This prevents state errors due
   to groups.

*  `\pydatasetfilehandle`, `\pydatareleasefilehandle`, `\pydatasetfilename`,
   and `\pydataclosefilename` are redesigned to deal with cases where the same
   file is opened, written, closed, and then later reopened and overwritten.
   `\pydatasetfilename` now reuses file handles when the same file is
   opened and closed multiple times.  `\pydataclosefilename` no longer
   attempts to close files `\AtEndDocument`, since that can interfere with
   files that need to remain open as long as possible.

*  Added new commands `\pydatawritekeyedefvalue` and
   `\pydatabufferkeyedefvalue`.  These `\edef` the value before interpreting
   it as verbatim text.

*  Added error messages for unknown file handles and file names.

*  Updated `tcblisting` usage in docs for compatibility with the latest
   `tcolorbox`.


## v0.1.0 (2023-11-19)

*  Initial release.
