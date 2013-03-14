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
from sarlacc.utils import _agi_parse_result


class TestCase(test.TestCase):

    def test_agi_parse_result_200_0(self):
        code, result, args = _agi_parse_result("200 result=0")
        self.assertEqual(code, '200')
        self.assertEqual(result, '0')
        self.assertEqual(args, '')

    def test_agi_parse_result_200_timeout(self):
        code, result, args = _agi_parse_result("200 result=0 (timeout)")
        self.assertEqual(code, '200')
        self.assertEqual(result, '0')
        self.assertEqual(args, '(timeout)')

    def test_agi_parse_result_200_timeout_fail(self):
        code, result, args = _agi_parse_result("200 result= (timeout)")
        self.assertEqual(code, '200')
        self.assertEqual(result, '')
        self.assertEqual(args, '(timeout)')

    def test_agi_parse_result_200_1(self):
        code, result, args = _agi_parse_result("200 result=1")
        self.assertEqual(code, '200')
        self.assertEqual(result, '1')
        self.assertEqual(args, '')

    def test_agi_parse_result_200_minus_1(self):
        code, result, args = _agi_parse_result("200 result=-1")
        self.assertEqual(code, '200')
        self.assertEqual(result, '-1')
        self.assertEqual(args, '')

    def test_agi_parse_result_520(self):
        code, result, args = _agi_parse_result(
            "520 Invalid command syntax.  Proper usage not available."
        )
        self.assertEqual(code, '520')
        self.assertEqual(
            result, "Invalid command syntax.  Proper usage not available."
        )
        self.assertEqual(args, '')
