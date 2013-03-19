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

    def test_receive_char_failure(self):
        with patch('sys.stdin', StringIO("200 result=-1 (hangup)")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf, timeout = self.agi.receive_char(timeout='100')
            self.assertEqual(mocked_out.getvalue(), 'RECEIVE CHAR 100\n')
            self.assertFalse(res)
            self.assertEqual(dtmf, '')
            self.assertFalse(timeout)

    def test_receive_char_success(self):
        with patch('sys.stdin', StringIO("200 result=221")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf, timeout = self.agi.receive_char(timeout='444')
            self.assertEqual(mocked_out.getvalue(), 'RECEIVE CHAR 444\n')
            self.assertTrue(res)
            self.assertEqual(dtmf, '221')
            self.assertFalse(timeout)

    def test_receive_char_timeout_without_digits(self):
        with patch('sys.stdin', StringIO("200 result= (timeout)")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf, timeout = self.agi.receive_char(timeout='11123')
            self.assertEqual(mocked_out.getvalue(), 'RECEIVE CHAR 11123\n')
            self.assertTrue(res)
            self.assertEqual(dtmf, '')
            self.assertTrue(timeout)

    def test_receive_char_timeout_with_digits(self):
        with patch('sys.stdin', StringIO("200 result=101 (timeout)")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf, timeout = self.agi.receive_char(timeout='2')
            self.assertEqual(mocked_out.getvalue(), 'RECEIVE CHAR 2\n')
            self.assertTrue(res)
            self.assertEqual(dtmf, '101')
            self.assertTrue(timeout)
