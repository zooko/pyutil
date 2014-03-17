# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-
from unittest import TestCase

from pyutil import jsonutil as json

class TestDefault(TestCase):
    def test_default(self):
        self.assertEquals(
            json.dumps(type, default=repr),
            json.dumps(repr(type)))
