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

import cStringIO
import mock

from sarlacc.tests.asterisk.agi import test


class TestCase(test.TestCase):

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=-1 (writefile)"))
    def test_record_file_failure_to_write(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, resp, endpos, dtmf = self.agi.record_file(
                filename='demo-congrats.gsm'
            )
            self.assertEqual(
                mock_stdout.getvalue(),
                'RECORD FILE demo-congrats.gsm "" "" "" BEEP\n')
            self.assertFalse(res)
            self.assertEqual(resp, 'writefile')
            self.assertEqual(endpos, '')
            self.assertEqual(dtmf, '')

    @mock.patch('sys.stdin', cStringIO.StringIO(
        "200 result=-1 (randomerror) endpos=22123")
    )
    def test_record_file_random_error(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, resp, endpos, dtmf = self.agi.record_file(
                filename='HelloWorld!'
            )
            self.assertEqual(
                mock_stdout.getvalue(),
                'RECORD FILE HelloWorld! "" "" "" BEEP\n')
            self.assertFalse(res)
            self.assertEqual(resp, 'randomerror')
            self.assertEqual(endpos, '22123')
            self.assertEqual(dtmf, '')

    @mock.patch('sys.stdin', cStringIO.StringIO(
        "200 result=-1 (waitfor) endpos=2111")
    )
    def test_record_file_failure_on_waitfor(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, resp, endpos, dtmf = self.agi.record_file(
                filename='HelloWorld!'
            )
            self.assertEqual(
                mock_stdout.getvalue(),
                'RECORD FILE HelloWorld! "" "" "" BEEP\n')
            self.assertFalse(res)
            self.assertEqual(resp, 'waitfor')
            self.assertEqual(endpos, '2111')
            self.assertEqual(dtmf, '')

    @mock.patch('sys.stdin', cStringIO.StringIO(
        "200 result=0 (hangup) endpos=223680")
    )
    def test_record_file_hangup(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, resp, endpos, dtmf = self.agi.record_file(
                filename='demo-congrats'
            )
            self.assertEqual(
                mock_stdout.getvalue(),
                'RECORD FILE demo-congrats "" "" "" BEEP\n')
            self.assertTrue(res)
            self.assertEqual(resp, 'hangup')
            self.assertEqual(endpos, '223680')
            self.assertEqual(dtmf, '')

    @mock.patch('sys.stdin', cStringIO.StringIO(
        "200 result=50 (dtmf) endpos=135297")
    )
    def test_record_file_digits_pressed(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, resp, endpos, dtmf = self.agi.record_file(
                filename='demo-congrats', digits='0123'
            )
            self.assertEqual(
                mock_stdout.getvalue(),
                'RECORD FILE demo-congrats "" "0123" "" BEEP\n')
            self.assertTrue(res)
            self.assertEqual(resp, 'dtmf')
            self.assertEqual(endpos, '135297')
            self.assertEqual(dtmf, '2')

    @mock.patch('sys.stdin', cStringIO.StringIO(
        "200 result=0 (timeout) endpos=13529")
    )
    def test_record_file_timeout(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, resp, endpos, dtmf = self.agi.record_file(
                filename='demo-congrats', fmt='wav', digits='0123',
                timeout='30', offset='3', beep=False, silence='1000'
            )
            self.assertEqual(
                mock_stdout.getvalue(),
                'RECORD FILE demo-congrats "wav" "0123" "30" "3" s=1000\n')
            self.assertTrue(res)
            self.assertEqual(resp, 'timeout')
            self.assertEqual(endpos, '13529')
            self.assertEqual(dtmf, '')
