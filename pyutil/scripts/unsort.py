#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

# randomize the lines of stdin or a file

import random, sys

def main():
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        inf = open(fname, 'r')
    else:
        inf = sys.stdin

    lines = inf.readlines()
    random.shuffle(lines)
    sys.stdout.writelines(lines)

if __name__ == '__main__':
    main()
