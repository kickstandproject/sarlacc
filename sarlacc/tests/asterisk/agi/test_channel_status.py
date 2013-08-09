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
    def test_channel_status_failure(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, status = self.agi.channel_status(name='Local/foo')
            self.assertEqual(
                mock_stdout.getvalue(), 'CHANNEL STATUS Local/foo\n'
            )
            self.assertFalse(res)
            self.assertEqual(status, '-1')

    @mock.patch('sys.stdin', cStringIO.StringIO("200 result=5"))
    def test_channel_status_success(self):
        with mock.patch(
                'sys.stdout', new_callable=cStringIO.StringIO) as mock_stdout:
            res, status = self.agi.channel_status(name='SIP/demo/123')
            self.assertEqual(
                mock_stdout.getvalue(), 'CHANNEL STATUS SIP/demo/123\n'
            )
            self.assertTrue(res)
            self.assertEqual(status, '5')
