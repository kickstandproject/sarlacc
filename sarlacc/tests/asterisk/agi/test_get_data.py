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

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=-1"))
    def test_get_data_failure(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, dtmf, timeout = self.agi.get_data(
                filename='demo-congrats.gsm', digits='0'
            )
            self.assertEqual(
                mock_stdout.getvalue(), 'GET DATA demo-congrats.gsm 0 0\n'
            )
            self.assertFalse(res)
            self.assertEqual(dtmf, '')
            self.assertFalse(timeout)

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=221"))
    def test_get_data_success(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, dtmf, timeout = self.agi.get_data(
                filename='demo-congrats', digits='1'
            )
            self.assertEqual(
                mock_stdout.getvalue(), 'GET DATA demo-congrats 0 1\n'
            )
            self.assertTrue(res)
            self.assertEqual(dtmf, '221')
            self.assertFalse(timeout)

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result= (timeout)"))
    def test_get_data_timeout_without_digits(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, dtmf, timeout = self.agi.get_data(
                filename='demo-congrats', digits='7'
            )
            self.assertEqual(
                mock_stdout.getvalue(), 'GET DATA demo-congrats 0 7\n'
            )
            self.assertTrue(res)
            self.assertEqual(dtmf, '')
            self.assertTrue(timeout)

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=101 (timeout)"))
    def test_get_data_timeout_with_digits(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, dtmf, timeout = self.agi.get_data(
                filename='demo-congrats', digits='2'
            )
            self.assertEqual(
                mock_stdout.getvalue(), 'GET DATA demo-congrats 0 2\n'
            )
            self.assertTrue(res)
            self.assertEqual(dtmf, '101')
            self.assertTrue(timeout)
