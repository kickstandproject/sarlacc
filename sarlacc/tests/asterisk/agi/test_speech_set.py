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

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=0"))
    def test_speech_set_failure(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res = self.agi.speech_set(name='foo', value='bar')
            self.assertEqual(mock_stdout.getvalue(), 'SPEECH SET foo bar\n')
            self.assertFalse(res)

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=1"))
    def test_speech_set_success(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res = self.agi.speech_set(name='enable', value='true')
            self.assertEqual(
                mock_stdout.getvalue(), 'SPEECH SET enable true\n'
            )
            self.assertTrue(res)
