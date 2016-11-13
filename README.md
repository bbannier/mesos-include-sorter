mesos-include-sorter
====================

This script can be used to sort includes according to the Mesos style.

Input lines are read from stdin, and written to stdout.

Current limitations
-------------------

* No filtering for `#include`-like lines; instead all lines would be sorted.
  Pass only `#include` lines to work around this.
* No special treatment for preprocessor macros inside the sorted range.
