# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-
from unittest import TestCase
from cStringIO import StringIO

from pyutil import jsonutil as json

class TestDump(TestCase):
    def test_dump(self):
        sio = StringIO()
        json.dump({}, sio)
        self.assertEquals(sio.getvalue(), '{}')

    def test_dumps(self):
        self.assertEquals(json.dumps({}), '{}')
