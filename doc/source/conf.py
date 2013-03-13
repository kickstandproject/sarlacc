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

import os
import sys

from sarlacc.version import SARLACC_VERSION as sarlacc_version

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../sarlacc/asterisk'))

extensions = ['sphinx.ext.autodoc']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'Sarlacc'
copyright = u'2013, Paul Belanger'
release = sarlacc_version.version_string_with_vcs()
version = sarlacc_version.canonical_version_string()
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'default'
htmlhelp_basename = 'sarlaccedoc'

latex_elements = {
}

latex_documents = [
  ('index', 'Sarlacc.tex', u'Sarlacc Documentation',
   u'Paul Belanger', 'manual'),
]

man_pages = [
    ('index', 'Sarlacc', u'Sarlacc Documentation',
     [u'Paul Belanger'], 1)
]

texinfo_documents = [
  ('index', 'Sarlacc', u'Sarlacc Documentation',
   u'Paul Belanger', 'Sarlacc', 'One line description of project.',
   'Miscellaneous'),
]
