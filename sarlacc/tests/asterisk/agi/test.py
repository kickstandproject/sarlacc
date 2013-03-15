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

from sarlacc.asterisk.agi import AGI
from sarlacc import test


class TestCase(test.TestCase):
    """Test case base class for all unit tests."""

    def setUp(self):
        """Run before each method to initialize test environment."""
        super(TestCase, self).setUp()
        self.agi = AGI()
