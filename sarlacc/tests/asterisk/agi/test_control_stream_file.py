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

    def test_control_stream_file_failure(self):
        with patch('sys.stdin', StringIO("200 result=-1")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf = self.agi.control_stream_file(
                filename='HelloWorld!'
            )
            self.assertEqual(
                mocked_out.getvalue(),
                'CONTROL STREAM FILE HelloWorld! "" "" "*" "#" ""\n')
            self.assertFalse(res)
            self.assertEqual(dtmf, '')

    def test_control_stream_file_success(self):
        with patch('sys.stdin', StringIO("200 result=0")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf = self.agi.control_stream_file(
                filename='demo-congrats'
            )
            self.assertEqual(
                mocked_out.getvalue(),
                'CONTROL STREAM FILE demo-congrats "" "" "*" "#" ""\n')
            self.assertTrue(res)
            self.assertEqual(dtmf, '')

    def test_control_stream_file_with_args_success(self):
        with patch('sys.stdin', StringIO("200 result=0")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf = self.agi.control_stream_file(
                filename='demo-congrats', skipms='1221', forward='1',
                rewind='3', pause='9',
            )
            self.assertEqual(
                mocked_out.getvalue(),
                'CONTROL STREAM FILE demo-congrats "" "1221" "1" "3" "9"\n')
            self.assertTrue(res)
            self.assertEqual(dtmf, '')

    def test_control_stream_file_digits_pressed(self):
        with patch('sys.stdin', StringIO("200 result=50")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, dtmf = self.agi.control_stream_file(
                filename='demo-congrats', digits='0123'
            )
            self.assertEqual(
                mocked_out.getvalue(),
                'CONTROL STREAM FILE demo-congrats "0123" "" "*" "#" ""\n')
            self.assertTrue(res)
            self.assertEqual(dtmf, '2')