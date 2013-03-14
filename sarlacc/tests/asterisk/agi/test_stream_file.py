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
from sarlacc import test
from sarlacc.asterisk.agi import AGI


class TestCase(test.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.agi = AGI()

    def test_stream_file_does_not_exist(self):
        with patch('sys.stdin', StringIO("200 result=0 endpos=0")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf, endpos = self.agi.stream_file('demo-congrats.gsm')
            self.assertEqual(
                mocked_out.getvalue(),
                'STREAM FILE demo-congrats.gsm "" 0\n')
            self.assertFalse(res)
            self.assertEqual(dtmf, '')
            self.assertEqual(endpos, '0')

    def test_stream_file_failure(self):
        with patch('sys.stdin', StringIO("200 result=-1 endpos=0")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf, endpos = self.agi.stream_file('HelloWorld!')
            self.assertEqual(
                mocked_out.getvalue(),
                'STREAM FILE HelloWorld! "" 0\n')
            self.assertFalse(res)
            self.assertEqual(dtmf, '')
            self.assertEqual(endpos, '0')

    def test_stream_file_success(self):
        with patch('sys.stdin', StringIO("200 result=0 endpos=223680")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf, endpos = self.agi.stream_file('demo-congrats')
            self.assertEqual(
                mocked_out.getvalue(),
                'STREAM FILE demo-congrats "" 0\n')
            self.assertTrue(res)
            self.assertEqual(dtmf, '')
            self.assertEqual(endpos, '223680')

    def test_stream_file_digits_pressed(self):
        with patch('sys.stdin', StringIO("200 result=50 endpos=135297")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf, endpos = self.agi.stream_file('demo-congrats', '0123')
            self.assertEqual(
                mocked_out.getvalue(),
                'STREAM FILE demo-congrats "0123" 0\n')
            self.assertTrue(res)
            self.assertEqual(dtmf, '2')
            self.assertEqual(endpos, '135297')
