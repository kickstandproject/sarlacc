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

"""
Utilities and helper functions
"""

import logging
import re
import sys

LOG = logging.getLogger(__name__)


def agi_send(data):
    sys.stdout.write("%s\n" % data)
    sys.stdout.flush()
    LOG.debug("agi_send: '%s'", data)
    code, result, args = _agi_read()

    return code, result, args


def _agi_read():
    res = sys.stdin.readline().strip()
    LOG.debug("_agi_read: '%s'", res)

    return _agi_parse_result(res)


def _agi_parse_result(data):
    pattern = r'(-?\d{0,3})\s?(.*)'
    match = re.match(pattern, data)

    if match:
        code = match.group(1)
        result = match.group(2)
        if code == '200':
            result = result.replace('result=', '')
            res, args = _agi_parse_result(result)[:2]

            return (code, res, args)
        return (code, result, '')
    else:
        return ('-255', '-99', '')


def agi_setup_env():
    env = {}
    while True:
        try:
            line = sys.stdin.readline().strip()
        except EOFError:
            break
        if not line:
            break
        data = line.split(":")

        if len(data) == 2:
            env[data[0].strip()] = data[1].strip()

    return env
