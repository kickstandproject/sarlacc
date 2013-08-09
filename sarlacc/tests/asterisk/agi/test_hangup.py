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
    def test_hangup_failure(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res = self.agi.hangup()
            self.assertEqual(mock_stdout.getvalue(), 'HANGUP\n')
            self.assertFalse(res)

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=1"))
    def test_hangup_success(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res = self.agi.hangup()
            self.assertEqual(mock_stdout.getvalue(), 'HANGUP\n')
            self.assertTrue(res)

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=1"))
    def test_hangup_success_with_args(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res = self.agi.hangup(channel='Local/1@public-03f5;1')
            self.assertEqual(
                mock_stdout.getvalue(), 'HANGUP Local/1@public-03f5;1\n'
            )
            self.assertTrue(res)
