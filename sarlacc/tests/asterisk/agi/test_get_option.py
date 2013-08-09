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

    @mock.patch('sys.stdin', cStringIO.StringIO(
        "200 result=0 endpos=0")
    )
    def test_get_option_does_not_exist(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, dtmf, endpos = self.agi.get_option(
                filename='demo-congrats.gsm'
            )
            self.assertEqual(
                mock_stdout.getvalue(),
                'GET OPTION demo-congrats.gsm "" 0\n')
            self.assertFalse(res)
            self.assertEqual(dtmf, '')
            self.assertEqual(endpos, '0')

    @mock.patch('sys.stdin', cStringIO.StringIO(
        "200 result=-1 endpos=0")
    )
    def test_get_option_failure(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, dtmf, endpos = self.agi.get_option(
                filename='HelloWorld!'
            )
            self.assertEqual(
                mock_stdout.getvalue(),
                'GET OPTION HelloWorld! "" 0\n')
            self.assertFalse(res)
            self.assertEqual(dtmf, '')
            self.assertEqual(endpos, '0')

    @mock.patch('sys.stdin', cStringIO.StringIO(
        "200 result=0 endpos=223680")
    )
    def test_get_option_success(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, dtmf, endpos = self.agi.get_option(
                filename='demo-congrats'
            )
            self.assertEqual(
                mock_stdout.getvalue(),
                'GET OPTION demo-congrats "" 0\n')
            self.assertTrue(res)
            self.assertEqual(dtmf, '')
            self.assertEqual(endpos, '223680')

    @mock.patch('sys.stdin', cStringIO.StringIO(
        "200 result=50 endpos=135297")
    )
    def test_get_option_digits_pressed(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, dtmf, endpos = self.agi.get_option(
                filename='demo-congrats', digits='0123'
            )
            self.assertEqual(
                mock_stdout.getvalue(),
                'GET OPTION demo-congrats "0123" 0\n')
            self.assertTrue(res)
            self.assertEqual(dtmf, '2')
            self.assertEqual(endpos, '135297')
