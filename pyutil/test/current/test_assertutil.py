#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

# Python Standard Library modules
import unittest

from pyutil import assertutil

class Testy(unittest.TestCase):
    def test_bad_precond(self):
        adict=23
        try:
            assertutil.precondition(isinstance(adict, dict), "adict is required to be a dict.", 23, adict=adict, foo=None)
        except AssertionError, le:
            self.failUnless(le.args[0] == "precondition: 'adict is required to be a dict.' <type 'str'>, 23 <type 'int'>, foo: None <type 'NoneType'>, 'adict': 23 <type 'int'>")
