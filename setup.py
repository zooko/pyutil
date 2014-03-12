#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

# pyutil -- utility functions and classes
#
# Author: Zooko Wilcox-O'Hearn
#
#  This file is part of pyutil; see `README.rst`_ for licensing terms.

import os, re, sys

from setuptools import find_packages, setup

trove_classifiers=[
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "License :: DFSG approved",
    "Intended Audience :: Developers",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: Unix",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: OS Independent",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Topic :: Utilities",
    "Topic :: Software Development :: Libraries",
    ]

PKG='pyutil'
VERSIONFILE = os.path.join(PKG, "_version.py")
verstr = "unknown"
try:
    verstrline = open(VERSIONFILE, "rt").read()
except EnvironmentError:
    pass # Okay, there is no version file.
else:
    VSRE = r"^verstr = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
    else:
        print "unable to find version in %s" % (VERSIONFILE,)
        raise RuntimeError("if %s.py exists, it must be well-formed" % (VERSIONFILE,))

doc_fnames=[ 'COPYING.SPL.txt', 'COPYING.GPL', 'COPYING.TGPPL.html', 'README.rst', 'CREDITS' ]

# In case we are building for a .deb with stdeb's sdist_dsc command, we put the
# docs in "share/doc/python-$PKG".
doc_loc = "share/doc/" + PKG

data_files = [
    (doc_loc, doc_fnames),
    (os.path.join('pyutil', 'data'), [os.path.join('pyutil', 'data', 'wordlist.txt')])
    ]

install_requires=['zbase32 >= 1.0']

readmetext_bytes = open('README.rst').read()
readmetext_unicode = readmetext_bytes.decode('utf-8')
while readmetext_unicode[0] == u'\ufeff':
    readmetext_unicode = readmetext_unicode[1:]

setup(name=PKG,
      version=verstr,
      description='a collection of utilities for Python programmers',
      long_description=readmetext_unicode,
      author="Zooko Wilcox-O'Hearn",
      author_email='zookog@gmail.com',
      url='https://tahoe-lafs.org/trac/' + PKG,
      license='GNU GPL', # see README.rst for details -- there are also alternative licences
      packages=find_packages(),
      include_package_data=True,
      data_files=data_files,
      extras_require={'jsonutil': ['simplejson >= 2.1.0',]},
      install_requires=install_requires,
      classifiers=trove_classifiers,
      entry_points = {
          'console_scripts': [
              'randcookie = pyutil.scripts.randcookie:main',
              'tailx = pyutil.scripts.tailx:main',
              'lines = pyutil.scripts.lines:main',
              'randfile = pyutil.scripts.randfile:main',
              'unsort = pyutil.scripts.unsort:main',
              'verinfo = pyutil.scripts.verinfo:main',
              'try_decoding = pyutil.scripts.try_decoding:main',
              'passphrase = pyutil.scripts.passphrase:main',
              ] },
      test_suite=PKG+".test",
      zip_safe=False, # I prefer unzipped for easier access.
      )
