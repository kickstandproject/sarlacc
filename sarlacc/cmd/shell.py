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

import sys

from cliff import app
from cliff import commandmanager

from sarlacc.common import utils
from sarlacc.openstack.common import log as logging
from sarlacc import version

LOG = logging.getLogger(__name__)


class Shell(app.App):

    def __init__(self):
        super(Shell, self).__init__(
            description='Sarlacc client', version=version.VERSION_INFO,
            command_manager=commandmanager.CommandManager('sarlacc.shell'),
        )

    def build_option_parser(self, description, version, argparse_kwargs=None):
        parser = super(Shell, self).build_option_parser(
            description, version, argparse_kwargs
        )
        parser.add_argument(
            '--os-asterisk-url',
            default=utils.env('OS_ASTERISK_URL'),
            help='Defaults to env[OS_ASTERISK_URL]',
        )

        parser.add_argument(
            '--os-asterisk-auth-username',
            default=utils.env('OS_ASTERISK_AUTH_USERNAME'),
            help='Defaults to env[OS_ASTERISK_AUTH_USERNAME]',
        )

        parser.add_argument(
            '--os-asterisk-auth-password',
            default=utils.env('OS_ASTERISK_AUTH_PASSWORD'),
            help='Defaults to env[OS_ASTERISK_AUTH_PASSWORD]',
        )

        return parser

    def prepare_to_run_command(self, cmd):
        super(Shell, self).prepare_to_run_command(cmd)

        if not self.options.os_asterisk_url:
            raise RuntimeError(
                'You must provide an Asterisk url via --os-asterisk-url or '
                'ENV[OS_ASTERISK_URL]'
            )
        if not self.options.os_asterisk_auth_username:
            raise RuntimeError(
                'You must provide an auth username via '
                '--os-asterisk-auth-username or ENV[OS_ASTERISK_AUTH_USERNAME]'
            )
        if not self.options.os_asterisk_auth_password:
            raise RuntimeError(
                'You must provide an auth password via '
                '--os-asterisk-auth-password or ENV[OS_ASTERISK_AUTH_PASSWORD]'
            )

        return


def main(argv=sys.argv[1:]):
    return Shell().run(argv)
