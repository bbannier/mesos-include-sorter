#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""FIXME(bbannier)."""

import fileinput
import re
from subprocess import Popen, PIPE

MAXIMUM = 80
GOAL = 70

def main():
    """FIXME(bbannier)."""
    comment_char = None

    comments = []

    for line in fileinput.input():
        if not comment_char:
            match = re.match(r'(\W+)(\w.*)', line)

            if not match:
                continue

            comment_char = match.group(1)

            comments.append(match.group(2))
        else:
            assert line.startswith(comment_char)

            comments.append(line[len(comment_char):])

    comments = [comment.rstrip() for comment in comments]

    offset = len(comment_char)
    goal = GOAL - offset
    maximum = MAXIMUM - offset

    fmt = Popen(
        ['fmt',
         '-s',
         '-d\'\'',
         str(goal),
         str(maximum),
         '/dev/stdin'],
        stdout=PIPE,
        stdin=PIPE,
        stderr=PIPE)

    formatted = fmt.communicate(input=' '.join(comments))[0]

    for line in formatted.splitlines():
        print '{}{}'.format(comment_char, line)

if __name__ == '__main__':
    main()
