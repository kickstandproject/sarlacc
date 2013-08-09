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
    def test_database_put_failure(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res = self.agi.database_put(
                family='Foo', key='Bar', value='example'
            )
            self.assertEqual(
                mock_stdout.getvalue(), 'DATABASE PUT Foo Bar example\n')
            self.assertFalse(res)

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=1"))
    def test_database_put_success(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res = self.agi.database_put(
                family='SIP', key='1001', value='Break'
            )
            self.assertEqual(
                mock_stdout.getvalue(), 'DATABASE PUT SIP 1001 Break\n'
            )
            self.assertTrue(res)
