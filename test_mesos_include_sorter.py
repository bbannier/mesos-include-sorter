#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Mesos include sorter."""

import subprocess


def sort(input_):
    """Invoke sorter on `lines`, return sorted lines."""
    process = subprocess.Popen(
        ['./mesos_include_sorter.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)

    output = process.communicate(input=input_.encode())[0]

    return output.decode()


def test_top_level_grouping():
    """Test that includes are grouped by high-level categories."""
    input_ = \
        '#include <project.hpp>\n' \
        '#include <string>\n' \
        '#include <string.h>\n'

    expected = \
        '#include <string.h>\n' \
        '\n' \
        '#include <string>\n' \
        '\n' \
        '#include <project.hpp>\n'

    assert sort(input_) == expected


def test_sorting():
    """Test alphabetic sorting inside a category."""
    input_ = \
        '#include <b.hpp>\n' \
        '#include <a.hpp>\n'

    expected = \
        '#include <a.hpp>\n' \
        '#include <b.hpp>\n'

    assert sort(input_) == expected


def test_depth_sectioning():
    """Test sectioning by file depth."""
    input_ = \
        '#include <a.hpp>\n' \
        '#include <a/a.hpp>\n' \
        '#include <b/b.hpp>\n' \
        '#include <b.hpp>\n'

    expected = \
        '#include <a.hpp>\n' \
        '#include <b.hpp>\n' \
        '\n' \
        '#include <a/a.hpp>\n' \
        '\n' \
        '#include <b/b.hpp>\n'

    assert sort(input_) == expected


def test_relatives_sorted():
    """Test sorting of files with relative paths."""
    input_ = \
        '#include "a.hpp"\n' \
        '#include <b.hpp>\n'

    expected = \
        '#include <b.hpp>\n' \
        '\n' \
        '#include "a.hpp"\n'

    assert sort(input_) == expected


def test_special_h_files():
    """
    Test treatment of special files ending in `.h` which are not system
    headers.
    """
    input_ = \
        '#include <string.h>\n' \
        '#include <gtest/gtest.h>\n'

    expected = \
        '#include <string.h>\n' \
        '\n' \
        '#include <gtest/gtest.h>\n'

    assert sort(input_) == expected


def test_empty_line_handling():
    """Test handling of empty lines."""
    input_ = \
        '#include <string>\n' \
        '\n' \
        '#include <string.h>\n'

    expected = \
        '#include <string.h>\n' \
        '\n' \
        '#include <string>\n'

    assert sort(input_) == expected
