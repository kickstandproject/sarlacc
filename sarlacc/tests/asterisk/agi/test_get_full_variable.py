# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2013 PolyBeacon, Inc.
#
# Author: Paul Belanger <paul.belanger@polybeacon.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cStringIO
import mock

from sarlacc.tests.asterisk.agi import test


class TestCase(test.TestCase):

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=0"))
    def test_get_full_variable_failure(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, value = self.agi.get_full_variable(name='FOO')
            self.assertEqual(
                mock_stdout.getvalue(), 'GET FULL VARIABLE FOO\n'
            )
            self.assertFalse(res)
            self.assertEqual(value, '')

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=1 (example.org)"))
    def test_get_full_variable_success(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, value = self.agi.get_full_variable(name='SIPDOMAIN')
            self.assertEqual(
                mock_stdout.getvalue(), 'GET FULL VARIABLE SIPDOMAIN\n'
            )
            self.assertTrue(res)
            self.assertEqual(value, 'example.org')

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=1 (bob)"))
    def test_get_full_variable_channel_success(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, value = self.agi.get_full_variable(
                name='ALICE', channel='Local/foo-bar'
            )
            self.assertEqual(
                mock_stdout.getvalue(),
                'GET FULL VARIABLE ALICE Local/foo-bar\n'
            )
            self.assertTrue(res)
            self.assertEqual(value, 'bob')
