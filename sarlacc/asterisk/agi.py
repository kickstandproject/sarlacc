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

"""
Asterisk AGI
"""

import re
import sys


class AGI(object):
    env = {}

    def __init__(self):
        self._setup_env()

    def answer(self):
        """
        Answers the channel.

        :returns:
            Failure: False
            Success: True
        """
        cmd = 'ANSWER'
        code, res = self._send(cmd)[:2]
        if res != 0:
            return False
        return True

    def get_variable(self, name):
        """
        Gets a channel variable.

        :param name:
            Channel name

        :type name:
            str

        :returns:
            String
        """
        cmd = 'GET VARIABLE %s' % name
        code, res, args = self._send(cmd)

        return res, args[1:-1]

    def hangup(self, channel=None):
        """
        Hangs up the specified channel.  If no channel is given, hangs up the
        current channel.

        :param channel:
            Name of the channel to hangup

        :type channel:
            str

        :returns:
            Failure: False
            Success: True
        """
        cmd = 'HANGUP'
        if channel is not None:
            cmd += ' %s' % channel
        code, res = self._send(cmd)[:2]

        if res != 1:
            return False
        return True

    def set_variable(self, name, value):
        """
        Sets a channel variable.

        :param name:
            Name of the channel variable

        :type name:
            str

        :param value:
            Value of the channel variable

        :type value:
            str

        :returns:
            Failure: False
            Success: True
        """
        cmd = 'SET VARIABLE %s %s' % (name, value)
        code, res = self._send(cmd)[:2]

        if res != 1:
            return False
        return True

    def verbose(self, level, message):
        """
        Log a message to the asterisk verbose log.

        :param level:
            Verbosity level

        :type level:
            int

        :param message:
            Text to be logged

        :type message:
            str

        :returns:
            Failure: False
            Success: True
        """
        cmd = 'VERBOSE "%s" %s' % (message, level)
        code, res = self._send(cmd)[:2]

        if res != 1:
            return False
        return True

    def _send(self, data):
        sys.stdout.write("%s\n" % data)
        sys.stdout.flush()
        code, result, args = self._read()
        return code, result, args

    def _read(self):
        res = sys.stdin.readline().strip()
        return self._parse_result(res)

    def _parse_result(self, data):
        pattern = r'(-?\d{1,3})\s?(.*)'
        match = re.match(pattern, data)
        if match:
            code = int(match.group(1))
            result = match.group(2)
            if code == 200:
                result = result.replace('result=', '')
                res, args = self._parse_result(result)[:2]
                return (code, res, args)
            return (code, result, '')
        else:
            return (100, -99, '')

    def _setup_env(self):
        while True:
            try:
                line = sys.stdin.readline().strip()
            except EOFError:
                break
            if not line:
                break
            data = line.split(":")
            if len(data) == 2:
                self.env[data[0].strip()] = data[1].strip()
