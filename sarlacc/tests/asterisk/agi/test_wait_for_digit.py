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

from cStringIO import StringIO
from mock import patch
from sarlacc.tests.asterisk.agi import test


class TestCase(test.TestCase):

    def test_wait_for_digit_failure(self):
        with patch('sys.stdin', StringIO("200 result=-1")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf = self.agi.wait_for_digit(timeout='2000')
            self.assertEqual(mocked_out.getvalue(), 'WAIT FOR DIGIT 2000\n')
            self.assertFalse(res)
            self.assertEqual(dtmf, '')

    def test_wait_for_digit_success(self):
        with patch('sys.stdin', StringIO("200 result=51")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf = self.agi.wait_for_digit(timeout='25000')
            self.assertEqual(mocked_out.getvalue(), 'WAIT FOR DIGIT 25000\n')
            self.assertTrue(res)
            self.assertEqual(dtmf, '3')

    def test_wait_for_digit_timeout(self):
        with patch('sys.stdin', StringIO("200 result=0")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf = self.agi.wait_for_digit(timeout='5000')
            self.assertEqual(mocked_out.getvalue(), 'WAIT FOR DIGIT 5000\n')
            self.assertTrue(res)
            self.assertEqual(dtmf, '')
