#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sorts lines containing include directives according to Mesos style."""

from __future__ import print_function

from itertools import groupby
import re
import sys


def depth_format(lines):
    """
    Sort `lines` with the Mesos per depth style.

    We assume that these headers already correspond to the same group.
    """
    def key(line):
        """The key is similar to the longest non-filename component."""
        components = line.split('/')
        return components[0:-1]

    lines.sort(key=key)

    groups = []
    for _, group in groupby(lines, key):
        groups.append(''.join(sorted(group)))

    return '\n'.join(groups)


def sort_format(lines):
    """Sort `lines` according to Mesos style."""
    def has_non_system_h_include(line):
        """Detect whether `line` includes a system header."""
        non_system_h_files = ['<gtest/gtest.h>', '<gmock/gmock.h>']
        return any([line.count(h) for h in non_system_h_files])

    system_headers = [l for l in lines if re.match(r'.*\.h>$', l) and
                      not has_non_system_h_include(l)]

    cppstdlib_headers = [l for l in lines if l.count('.') == 0]

    absolute_project_headers = [l for l in lines
                                if re.match(r'.*\.hpp>$', l)
                                or has_non_system_h_include(l)]

    rest = list(
        set(lines).difference(
            system_headers +
            cppstdlib_headers +
            absolute_project_headers))

    results = []

    if system_headers:
        results.append(''.join(depth_format(system_headers)))

    if cppstdlib_headers:
        results.append(''.join(depth_format(cppstdlib_headers)))

    if absolute_project_headers:
        results.append(''.join(depth_format(absolute_project_headers)))

    if rest:
        results.append(''.join(depth_format(rest)))

    return '\n'.join(results)


if __name__ == '__main__':
    # TODO(bbannier): support working on arbitrary code, just sorting includes.
    # TODO(bbannier): respect proprocessor macros surrounding includes.
    INCLUDES = [LINE for LINE in sys.stdin.readlines() if LINE != '\n']
    print(sort_format(INCLUDES), end='')
