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

import base64

from cliff import show

from sarlacc.asterisk.ari import client
from sarlacc.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class AsteriskInfo(show.ShowOne):

    def take_action(self, parsed_args, model):
        endpoint = '%s/%s' % (self.app_args.os_asterisk_url, 'ari')
        username = self.app_args.os_asterisk_auth_username
        password = self.app_args.os_asterisk_auth_password
        auth = base64.encodestring(
            '%s:%s' % (username, password)
        ).replace('\n', '')
        kwargs = {
            'token': 'Basic %s' % auth,
        }
        self.http_client = client.Client(endpoint, **kwargs)
        data = self.http_client.asterisk.info()

        return zip(*sorted(data[model].items()))


class ShowBuildInfo(AsteriskInfo):

    def take_action(self, parsed_args):
        model = 'build'

        result = super(ShowBuildInfo, self).take_action(
            parsed_args=parsed_args, model=model
        )

        return result


class ShowConfigInfo(AsteriskInfo):

    def take_action(self, parsed_args):
        model = 'config'

        result = super(ShowConfigInfo, self).take_action(
            parsed_args=parsed_args, model=model
        )

        return result


class ShowStatusInfo(AsteriskInfo):

    def take_action(self, parsed_args):
        model = 'status'

        result = super(ShowStatusInfo, self).take_action(
            parsed_args=parsed_args, model=model
        )

        return result


class ShowSystemInfo(AsteriskInfo):

    def take_action(self, parsed_args):
        model = 'system'

        result = super(ShowSystemInfo, self).take_action(
            parsed_args=parsed_args, model=model
        )

        return result
