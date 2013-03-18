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

    def test_get_full_variable_failure(self):
        with patch('sys.stdin', StringIO("200 result=0")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, value = self.agi.get_full_variable(name='FOO')
            self.assertEqual(
                mocked_out.getvalue(), 'GET FULL VARIABLE FOO\n'
            )
            self.assertFalse(res)
            self.assertEqual(value, '')

    def test_get_full_variable_success(self):
        with patch('sys.stdin', StringIO("200 result=1 (example.org)")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, value = self.agi.get_full_variable(name='SIPDOMAIN')
            self.assertEqual(
                mocked_out.getvalue(), 'GET FULL VARIABLE SIPDOMAIN\n'
            )
            self.assertTrue(res)
            self.assertEqual(value, 'example.org')

    def test_get_full_variable_channel_success(self):
        with patch('sys.stdin', StringIO("200 result=1 (bob)")
                   ), patch('sys.stdout',
                            new_callable=StringIO) as mocked_out:
            res, value = self.agi.get_full_variable(
                name='ALICE', channel='Local/foo-bar'
            )
            self.assertEqual(
                mocked_out.getvalue(),
                'GET FULL VARIABLE ALICE Local/foo-bar\n'
            )
            self.assertTrue(res)
            self.assertEqual(value, 'bob')
