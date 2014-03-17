#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

# pyutil -- utility functions and classes
#
# This file is part of pyutil; see README.rst for licensing terms.

import os, re, sys

from setuptools import find_packages, setup

trove_classifiers=[
    u"Development Status :: 5 - Production/Stable",
    u"License :: OSI Approved :: GNU General Public License (GPL)",
    u"License :: DFSG approved",
    u"Intended Audience :: Developers",
    u"Operating System :: Microsoft :: Windows",
    u"Operating System :: Unix",
    u"Operating System :: MacOS :: MacOS X",
    u"Operating System :: OS Independent",
    u"Natural Language :: English",
    u"Programming Language :: Python",
    u"Programming Language :: Python :: 2",
    u"Programming Language :: Python :: 2.7",
    u"Topic :: Utilities",
    u"Topic :: Software Development :: Libraries",
    ]

PKG=u'pyutil'
VERSIONFILE = os.path.join(PKG, u"_version.py")

import versioneer
versioneer.versionfile_source = VERSIONFILE
versioneer.versionfile_build = VERSIONFILE
versioneer.tag_prefix = PKG+u'-' # tags are like pyutil-1.2.0
versioneer.parentdir_prefix = PKG+u'-' # dirname like 'myproject-1.2.0'

doc_fnames=[ u'COPYING.SPL.txt', u'COPYING.GPL', u'COPYING.TGPPL.rst', u'README.rst', u'CREDITS' ]

# In case we are building for a .deb with stdeb's sdist_dsc command, we put the
# docs in "share/doc/python-$PKG".
doc_loc = u"share/doc/" + PKG

data_files = [
    (doc_loc, doc_fnames),
    (os.path.join(u'pyutil', u'data'), [os.path.join(u'pyutil', u'data', u'wordlist.txt')])
    ]

install_requires=[u'zbase32 >= 1.0']

readmetext_bytes = open(u'README.rst').read()
readmetext_unicode = readmetext_bytes.decode('utf-8')
while readmetext_unicode[0] == u'\ufeff':
    readmetext_unicode = readmetext_unicode[1:]

setup(name=PKG,
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description=u'a collection of utilities for Python programmers',
      long_description=readmetext_unicode,
      author=u"Zooko Wilcox-O'Hearn",
      author_email=u'zookog@gmail.com',
      url=u'https://tahoe-lafs.org/trac/' + PKG,
      license=u'GNU GPL', # see README.rst for details -- there are also alternative licences
      packages=find_packages(),
      include_package_data=True,
      data_files=data_files,
      extras_require={u'jsonutil': [u'simplejson >= 2.1.0',]},
      install_requires=install_requires,
      classifiers=trove_classifiers,
      entry_points = {
          u'console_scripts': [
              u'randcookie = pyutil.scripts.randcookie:main',
              u'tailx = pyutil.scripts.tailx:main',
              u'lines = pyutil.scripts.lines:main',
              u'randfile = pyutil.scripts.randfile:main',
              u'unsort = pyutil.scripts.unsort:main',
              u'verinfo = pyutil.scripts.verinfo:main',
              u'try_decoding = pyutil.scripts.try_decoding:main',
              u'passphrase = pyutil.scripts.passphrase:main',
              ] },
      test_suite=PKG+u".test",
      zip_safe=False, # I prefer unzipped for easier access.
      )
