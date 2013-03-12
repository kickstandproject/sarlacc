#!/usr/bin/env python

# Copyright (C) 2013 PolyBeacon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.

import setuptools

from sarlacc.openstack.common import setup
from sarlacc.version import SARLACC_VERSION as version


requires = setup.parse_requirements()
test_requires = setup.parse_requirements(['tools/test-requires'])
depend_links = setup.parse_dependency_links()

setuptools.setup(
    name='sarlacc',
    version=version.canonical_version_string(always=True),
    author='Paul Belanger',
    author_email='paul.belanger@polybeacon.com',
    url='https://github.com/kickstandproject/sarlacc',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    cmdclass=setup.get_cmdclass(),
    install_requires=requires,
    setup_requires=['setuptools_git>=0.4'],
    dependency_links=depend_links,
    zip_safe=False
)
