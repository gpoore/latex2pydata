# Changelog — latex2pydata LaTeX package


## v0.6.0 (2025/03/26)

*  `\pydatasetfilename` now automatically reuses file handles when files are
   closed, so that the total number of file handles created is never more than
   the maximum number of files open simultaneously.  This minimizes the
   potential for "`No more room for a new \write`" errors.  Previously, one
   file handle was created per file (#2).



## v0.5.0 (2025/03/03)

*  Renamed schema missing setting `rawstr` to `verbatim`.

*  Improved schema documentation.

*  Renamed `*mlvaluestart` macros to `*mlvalueopen` and renamed `*mlvalueend`
   macros to `*mlvalueclose`, so that `mlvalue` macros are consistent with
   `dict` and `list` macros for handling opening/closing delimiters.  The old
   macros are retained for now for backward compatibility.



## v0.4.0 (2024/11/17)

*  Replaced buffer index counter with a macro to prevent issues with commands
   and environments such as `\text` from `amsmath` that modify counter
   behavior.



## v0.3.0 (2024/10/16)

*  Replaced buffer length counters with macros to prevent issues with
   `\includeonly` resetting counters.



## v0.2.0 (2024-05-16)

*  Operations on file handles, file names, and buffers are now global.
   This prevents errors due to groups.

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

*  Simplified implementation of `pydatabuffermlvalue` environment, based on
   latest `fvextra`.

*  Added error messages for unknown file handles and file names.

*  Added additional state and data checks in `\pydatawritebuffer`.

*  Added documentation for `\pydatawritemlvaluestart`,
   `\pydatawritemlvalueline`, `\pydatawritemlvalueend`,
   `\pydatabuffermlvaluestart`, `\pydatabuffermlvalueline`,
   `\pydatabuffermlvalueend`.

*  Updated `tcblisting` usage in docs for compatibility with the latest
   `tcolorbox`.



## v0.1.0 (2023-11-19)

*  Initial release.
