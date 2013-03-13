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

from sarlacc import test
from sarlacc.asterisk.agi import AGI


class AGITestCase(test.TestCase):

    def setUp(self):
        super(AGITestCase, self).setUp()
        self.agi = AGI()

    def test_parse_result_200_0(self):
        code, result, args = self.agi._parse_result("200 result=0")
        self.assertEqual(code, 200)
        self.assertEqual(result, 0)
        self.assertEqual(args, '')

    def test_parse_result_200_timeout(self):
        code, result, args = self.agi._parse_result("200 result=0 (timeout)")
        self.assertEqual(code, 200)
        self.assertEqual(result, 0)
        self.assertEqual(args, '(timeout)')

    def test_parse_result_200_1(self):
        code, result, args = self.agi._parse_result("200 result=1")
        self.assertEqual(code, 200)
        self.assertEqual(result, 1)
        self.assertEqual(args, '')

    def test_parse_result_200_minus_1(self):
        code, result, args = self.agi._parse_result("200 result=-1")
        self.assertEqual(code, 200)
        self.assertEqual(result, -1)
        self.assertEqual(args, '')

    def test_parse_result_520(self):
        code, result, args = self.agi._parse_result(
            "520 Invalid command syntax.  Proper usage not available."
        )
        self.assertEqual(code, 520)
        self.assertEqual(
            result, "Invalid command syntax.  Proper usage not available."
        )
        self.assertEqual(args, '')
