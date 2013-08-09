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

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=-1"))
    def test_say_time_failure(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, dtmf = self.agi.say_time(epoch='1363725155')
            self.assertEqual(
                mock_stdout.getvalue(), 'SAY TIME 1363725155 ""\n'
            )
            self.assertFalse(res)
            self.assertEqual(dtmf, '')

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=0"))
    def test_say_time_success(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, dtmf = self.agi.say_time(epoch='1363725172')
            self.assertEqual(
                mock_stdout.getvalue(), 'SAY TIME 1363725172 ""\n'
            )
            self.assertTrue(res)
            self.assertEqual(dtmf, '')

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=49"))
    def test_say_time_digit_pressed(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, dtmf = self.agi.say_time(epoch='1363725192', digits='1234')
            self.assertEqual(
                mock_stdout.getvalue(), 'SAY TIME 1363725192 "1234"\n'
            )
            self.assertTrue(res)
            self.assertEqual(dtmf, '1')
