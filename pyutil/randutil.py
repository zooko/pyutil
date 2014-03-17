# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

import warnings
import os, random

class devrandomRandom(random.Random):
    """ The problem with using this one, of course, is that it blocks.  This
    is, of course, a security flaw.  (On Linux and probably on other
    systems.) --Zooko 2005-03-04

    Not repeatable.
    """
    def __init__(self):
        warnings.warn("deprecated", DeprecationWarning)
        self.dr = open("/dev/random", "r")

    def get(self, bytes):
        return self.dr.read(bytes)


class devurandomRandom(random.Random):
    """ The problem with using this one is that it gives answers even when it
    has never been properly seeded, e.g. when you are booting from CD and have
    just started up and haven't yet gathered enough entropy to actually be
    unguessable.  (On Linux and probably on other systems.)  --Zooko 2005-03-04

    Not repeatable.
    """
    def get(self, bytes):
        warnings.warn("deprecated", DeprecationWarning)
        return os.urandom(bytes)


randobj = devurandomRandom()
get = randobj.get
random = randobj.random
randrange = randobj.randrange
shuffle = randobj.shuffle
choice = randobj.choice
seed = randobj.seed

def randstr(n):
    return ''.join(map(chr, map(randrange, [0]*n, [256]*n)))

def insecurerandstr(n):
    return os.urandom(n)
