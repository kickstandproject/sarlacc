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

import logging
from sarlacc.utils import agi_send, agi_setup_env

LOG = logging.getLogger(__name__)


class AGI(object):
    env = {}

    def __init__(self):
        self.env = agi_setup_env()

    def answer(self):
        """
        Answers the channel.

        :returns:
            bool
        """
        cmd = 'ANSWER'
        res = agi_send(cmd)[1]
        if res != '0':
            return False
        return True

    def asyncagi_break(self):
        """
        Interrupt Async AGI.

        :returns:
            bool
        """

        cmd = 'ASYNCAGI BREAK'
        agi_send(cmd)

        return True

    def channel_status(self, name):
        """
        Returns the status of the connected channel.

        :param name:

        :type name:
            str

        :returns:
            bool, string
        """
        result = True

        cmd = 'CHANNEL STATUS %s' % (name)
        res = agi_send(cmd)[1]

        if res == '-1':
            result = False

        return result, res

    def control_stream_file(
            self, filename, digits='', skipms='', forward='*', rewind='#',
            pause=''):
        """
        Plays the audio file to the current channel.

        :param filename:
            Filename to play.  The extension must not be included in the
            filename.

        :type filename:
            str

        :param digits:
            Digits to interrupt audio stream.

        :type digits:
            str

        :param skipms:

        :type skipms:
            str

        :param forward:

        :type forward:
            str

        :param rewind:

        :type rewind:
            str

        :param pause:

        :type pause:
            str

        :returns:
            bool, string
        """
        cmd = 'CONTROL STREAM FILE %s "%s" "%s" "%s" "%s" "%s"' % (filename,
                                                                   digits,
                                                                   skipms,
                                                                   forward,
                                                                   rewind,
                                                                   pause)

        return self._parse_digit_response(cmd)

    def database_del(self, family, key):
        """
        Remove database key / value.

        :param family:

        :type family:
            str

        :param key:

        :type key:
            str

        :returns:
            bool
        """
        cmd = 'DATABASE DEL %s %s' % (family, key)
        res = agi_send(cmd)[1]
        if res != '1':
            return False
        return True

    def database_deltree(self, family, keytree):
        """
        Remove database keytree / value.

        :param family:

        :type family:
            str

        :param keytree:

        :type keytree:
            str

        :returns:
            bool
        """
        cmd = 'DATABASE DELTREE %s %s' % (family, keytree)
        res = agi_send(cmd)[1]
        if res != '1':
            return False
        return True

    def database_get(self, family, key):
        """
        Get database value.

        :param family:

        :type family:
            str

        :param key:

        :type key:
            str

        :returns:
            bool
        """
        cmd = 'DATABASE GET %s %s' % (family, key)
        res, args = agi_send(cmd)[1:]

        if res != '1':
            return False, ''

        return True, args[1:-1]

    def database_put(self, family, key, value):
        """
        Adds / updates database value.

        :param family:

        :type family:
            str

        :param key:

        :type key:
            str

        :param value:

        :type value:
            str

        :returns:
            bool
        """
        cmd = 'DATABASE PUT %s %s %s' % (family, key, value)
        res = agi_send(cmd)[1]
        if res != '1':
            return False
        return True

    def execute(self, application, options=''):
        """
        Execute a given application.

        :param application:
            Name of the Asterisk application.

        :type application:
            str

        :param options:
            A comma delimited string of your applications options.

        :type options:
            str

        :returns:
            bool, string
        """
        cmd = 'EXEC %s' % application
        if options != '':
            cmd += ' %s' % options

        res = agi_send(cmd)[1]
        if res == '-2':
            return False, ''
        return True, res

    def get_data(self, filename, digits, timeout='0'):
        """
        Plays the audio file to the current channel.

        :param filename:
            Name of the file you wish to be played. The extension must not be
            included in the filename.

        :type filename:
            str

        :param digits:
            Maximum number of digits the user can enter. Note: The value must
            be greater the 0 otherwise asterisk will return failure.

        :type digits:
            str

        :param timeout:
            The amount of time, in milliseconds, to wait after the last DTMF is
            recieved.

        :type timeout:
            str

        :returns:
            bool, string, string
        """
        cmd = 'GET DATA %s %s %s' % (filename, timeout, digits)

        return self._parse_timeout_response(cmd)

    def get_full_variable(self, name, channel=''):
        """
        Evaluates a channel expression.

        :param name:
            Variable name.

        :type name:
            str

        :param channel:

        :type options:
            str

        :returns:
            bool, string
        """
        cmd = 'GET FULL VARIABLE %s' % name
        if channel != '':
            cmd += ' %s' % channel

        res, args = agi_send(cmd)[1:]
        if res != '1':
            return False, ''

        return True, args[1:-1]

    def get_option(self, filename, digits='', timeout='0'):
        """
        Plays the audio file to the current channel.

        :param filename:
            Filename to play.  The extension must not be included in the
            filename.

        :type filename:
            str

        :param digits:
            Digits to interrupt audio stream.

        :type digits:
            str

        :param timeout:
            The amount of time, in milliseconds, to wait after the last DTMF is
            recieved.

        :type timeout:
            str

        :returns:
            bool, string
        """
        cmd = 'GET OPTION %s "%s" %s' % (filename, digits, timeout)

        return self._parse_get_option_or_stream_file(cmd)

    def get_variable(self, name):
        """
        Gets a channel variable.

        :param name:
            Channel name

        :type name:
            str

        :returns:
            bool, string
        """
        cmd = 'GET VARIABLE %s' % name
        res, args = agi_send(cmd)[1:]

        if res != '1':
            return False, ''

        return True, args[1:-1]

    def hangup(self, channel=None):
        """
        Hangs up the specified channel.  If no channel is given, hangs up the
        current channel.

        :param channel:
            Name of the channel to hangup

        :type channel:
            str

        :returns:
            bool
        """
        cmd = 'HANGUP'
        if channel is not None:
            cmd += ' %s' % channel
        res = agi_send(cmd)[1]

        if res != '1':
            return False

        return True

    def noop(self):
        """
        Do nothing.

        This function does nothing.

        :returns:
            bool
        """
        cmd = 'NOOP'
        agi_send(cmd)

        return True

    def receive_char(self, timeout):
        """
        Receive one character from channels support it.

        :param timeout:
            The amount of time, in milliseconds, to wait for DTMF.

        :type timeout:
            str

        :returns:
            bool, str, str
        """
        cmd = 'RECEIVE CHAR %s' % timeout

        return self._parse_timeout_response(cmd)

    def receive_text(self, timeout):
        """
        Receives text from channels supporting it.

        :param timeout:
            The amount of time, in milliseconds, to wait for DTMF.

        :type timeout:
            str

        :returns:
            bool, str
        """
        cmd = 'RECEIVE TEXT %s' % timeout
        res, args = agi_send(cmd)[1:]

        if res != '1':
            return False, ''

        return True, args[1:-1]

    def record_file(
            self, filename, fmt='', digits='', timeout='', offset='',
            beep=True, silence=''):
        """
        Plays the audio file to the current channel.

        :param filename:
            Filename to play.  The extension must not be included in the
            filename.

        :type filename:
            str

        :param fmt:

        :type fmt:
            str

        :param digits:
            Digits to interrupt audio stream.

        :type digits:
            str

        :param timeout:

        :type timeout:
            str

        :param offset:

        :type offset:
            str

        :param beep:

        :type beep:
            bool

        :param beep:

        :type beep:
            bool

        :returns:
            bool, string
        """
        result = True
        dtmf = ''
        endpos = ''

        cmd = 'RECORD FILE %s "%s" "%s" "%s"' % (filename, fmt, digits,
                                                 timeout)
        if offset != '':
            cmd += ' "%s"' % offset
        if beep:
            cmd += ' BEEP'
        if silence != '':
            cmd += ' s=%s' % silence

        res, args = agi_send(cmd)[1:]
        resp = args

        if ' ' in args:
            resp, endpos = args.split(' ')
            endpos = endpos.replace('endpos=', '')

        if res == '-1':
            result = False
        elif res == '0' and endpos == '0':
            result = False
        if res > '0':
            dtmf = chr(int(res))

        return result, resp[1:-1], endpos, dtmf

    def say_alpha(self, string, digits=''):
        """
        Say a given character string.

        :param string:

        :type string:
            str

        :param digits:
            Digits to interrupt audio stream.

        :type digits:
            str

        :returns:
            bool, str

        """
        cmd = 'SAY ALPHA %s "%s"' % (string, digits)

        return self._parse_digit_response(cmd)

    def say_date(self, epoch, digits=''):
        """
        Say a given date.

        :param epoch:

        :type epoch:
            str

        :param digits:
            Digits to interrupt audio stream.

        :type digits:
            str

        :returns:
            bool, str

        """
        cmd = 'SAY DATE %s "%s"' % (epoch, digits)

        return self._parse_digit_response(cmd)

    def say_datetime(self, epoch, digits='', fmt='', timezone=''):
        """
        Say a given time as specified by the format given.

        :param epoch:

        :type epoch:
            str

        :param digits:
            Digits to interrupt audio stream.

        :type digits:
            str

        :param fmt:

        :type fmt:
            str

        :param timezone:

        :type timezone:
            str

        :returns:
            bool, str

        """
        cmd = 'SAY DATETIME %s "%s" "%s" "%s"' % (epoch, digits, fmt,
                                                  timezone)

        return self._parse_digit_response(cmd)

    def say_digits(self, string, digits=''):
        """
        Say a given digit string.

        :param string:

        :type string:
            str

        :param digits:
            Digits to interrupt audio stream.

        :type digits:
            str

        :returns:
            bool, str

        """
        cmd = 'SAY DIGITS %s "%s"' % (string, digits)

        return self._parse_digit_response(cmd)

    def say_number(self, string, digits='', gender=None):
        """
        Say a given number.

        :param string:

        :type string:
            str

        :param digits:
            Digits to interrupt audio stream.

        :type digits:
            str

        :param gender:
            Set to 'f' for female or 'm' for male.

        :type digits:
            str

        :returns:
            bool, str

        """
        cmd = 'SAY NUMBER %s "%s"' % (string, digits)
        if gender is True:
            cmd += ' m'
        elif gender is False:
            cmd += ' f'

        return self._parse_digit_response(cmd)

    def say_phonetic(self, string, digits=''):
        """
        Say a given character string with phonetics.

        :param string:

        :type number:
            str

        :param digits:
            Digits to interrupt audio stream.

        :type digits:
            str

        :returns:
            bool, str

        """
        cmd = 'SAY PHONETIC %s "%s"' % (string, digits)

        return self._parse_digit_response(cmd)

    def say_time(self, epoch, digits=''):
        """
        Say a given time.

        :param epoch:

        :type epoch:
            str

        :param digits:
            Digits to interrupt audio stream.

        :type digits:
            str

        :returns:
            bool, str

        """
        cmd = 'SAY TIME %s "%s"' % (epoch, digits)

        return self._parse_digit_response(cmd)

    def send_image(self, filename):
        """
        Sends images to channels supporting it.

        :param filename:

        :type filename:
            str

        :returns:
            bool
        """
        cmd = 'SEND IMAGE %s' % filename
        res = agi_send(cmd)[1]
        if res != '0':
            return False
        return True

    def send_text(self, message):
        """
        Sends text to channels supporting it.

        :param message:

        :type message:
            str

        :returns:
            bool
        """
        cmd = 'SEND TEXT "%s"' % message
        res = agi_send(cmd)[1]
        if res != '0':
            return False
        return True

    def set_auto_hangup(self, time):
        """
        Hangup the current channel some time in the future.

        :param time:
            Amount of seconds in the future.

        :type time:
            str

        :returns:
            bool
        """
        cmd = 'SET AUTOHANGUP %s' % (time)
        agi_send(cmd)

        return True

    def set_caller_id(self, number):
        """
        Sets caller id for the current channel.

        :param number:

        :type number:
            str

        :returns:
            bool
        """
        cmd = 'SET CALLERID %s' % number
        agi_send(cmd)

        return True

    def set_context(self, string):
        """
        Sets dialplan context.

        :param string:

        :type string:
            str

        :returns:
            bool
        """
        cmd = 'SET CONTEXT %s' % string
        agi_send(cmd)

        return True

    def set_extension(self, string):
        """
        Sets dialplan extension.

        :param string:

        :type string:
            str

        :returns:
            bool
        """
        cmd = 'SET EXTENSION %s' % string
        agi_send(cmd)

        return True

    def set_music(self, enable=True, string=''):
        """
        Enable / disable music on hold generator.

        :param enable:

        :type enable:
            bool

        :param string:

        :type string:
            str

        :returns:
            bool
        """
        tmp = 'on'

        if not enable:
            tmp = 'off'
        cmd = 'SET MUSIC %s' % tmp

        if string != '':
            cmd += ' %s' % string
        agi_send(cmd)

        return True

    def set_priority(self, string):
        """
        Sets dialplan priority.

        :param string:

        :type string:
            str

        :returns:
            bool
        """
        cmd = 'SET PRIORITY %s' % string
        agi_send(cmd)

        return True

    def set_variable(self, name, value):
        """
        Set channel variable.

        :param name:

        :type name:
            str

        :param value:

        :type value:
            str

        :returns:
            bool
        """
        cmd = 'SET VARIABLE %s %s' % (name, value)
        agi_send(cmd)

        return True

    def stream_file(self, filename, digits='', offset='0'):
        """
        Plays the audio file to the current channel.

        :param filename:
            Filename to play.  The extension must not be included in the
            filename.

        :type filename:
            str

        :param digits:
            Digits to interrupt audio stream.

        :type digits:
            str

        :param offset:
            If an offset is provided the audio will seek to the offset before
            play starts.

        :type offset:
            str

        :returns:
            bool
        """
        cmd = 'STREAM FILE %s "%s" %s' % (filename, digits, offset)

        return self._parse_get_option_or_stream_file(cmd)

    def speech_activate_grammar(self, name):
        """
        Activates a grammar.

        :param name:

        :type name:
            str

        :returns:
            bool
        """
        cmd = 'SPEECH ACTIVATE GRAMMAR %s' % name
        res = agi_send(cmd)[1]
        if res != '1':
            return False

        return True

    def speech_create(self, engine):
        """
        Creates a speech object.

        :param engine:

        :type engine:
            str

        :returns:
            bool
        """
        cmd = 'SPEECH CREATE %s' % engine
        res = agi_send(cmd)[1]
        if res != '1':
            return False

        return True

    def speech_deactivate_grammar(self, name):
        """
        Deactivates a grammar.

        :param name:

        :type name:
            str

        :returns:
            bool
        """
        cmd = 'SPEECH DEACTIVATE GRAMMAR %s' % name
        res = agi_send(cmd)[1]
        if res != '1':
            return False

        return True

    def speech_destroy(self):
        """
        Destroys a speech object.

        :returns:
            bool
        """
        cmd = 'SPEECH DESTROY'
        res = agi_send(cmd)[1]
        if res != '1':
            return False

        return True

    def speech_load_grammar(self, name, path):
        """
        Loads a grammar.

        :param name:

        :type name:
            str

        :param path:

        :type path:
            str

        :returns:
            bool
        """
        cmd = 'SPEECH LOAD GRAMMAR %s %s' % (name, path)
        res = agi_send(cmd)[1]
        if res != '1':
            return False

        return True

    def speech_set(self, name, value):
        """
        Sets a speech engine setting.

        :param name:

        :type name:
            str

        :param value:

        :type value:
            str

        :returns:
            bool
        """
        cmd = 'SPEECH SET %s %s' % (name, value)
        res = agi_send(cmd)[1]
        if res != '1':
            return False

        return True

    def speech_unload_grammar(self, name):
        """
        Loads a grammar.

        :param name:

        :type name:
            str

        :returns:
            bool
        """
        cmd = 'SPEECH UNLOAD GRAMMAR %s' % name
        res = agi_send(cmd)[1]
        if res != '1':
            return False

        return True

    def tdd_mode(self, string):
        """
        Toggles telecommunications device for the deaf support.

        :param string:

        :type string:
            str

        :returns:
            bool
        """
        cmd = 'TDD MODE %s' % string
        res = agi_send(cmd)[1]
        if res != '1':
            return False
        return True

    def verbose(self, level, message):
        """
        Log a message to the asterisk verbose log.

        :param level:
            Verbosity level.

        :type level:
            int

        :param message:
            Output text message.

        :type message:
            str

        :returns:
            bool
        """
        cmd = 'VERBOSE "%s" %s' % (message, level)
        agi_send(cmd)

        return True

    def wait_for_digit(self, timeout):
        """
        Wait up to x amount of milliseconds for channel to receive a DTMF
        digit.

        :param timeout:
            The amount of time, in milliseconds, to wait for DTMF.

        :type timeout:
            str

        :returns:
            bool, string
        """
        cmd = 'WAIT FOR DIGIT %s' % timeout

        return self._parse_digit_response(cmd)

    def _parse_digit_response(self, cmd):
        result = True
        digit = ''

        res = agi_send(cmd)[1]

        if res == '-1':
            result = False
        elif res > '0':
            digit = chr(int(res))

        return result, digit

    def _parse_get_option_or_stream_file(self, cmd):
        result = True
        dtmf = ''

        res, args = agi_send(cmd)[1:]
        endpos = args.replace('endpos=', '')

        if res == '-1':
            result = False
        elif res == '0' and endpos == '0':
            result = False
        if res > '0':
            dtmf = chr(int(res))

        return result, dtmf, endpos

    def _parse_timeout_response(self, cmd):
        ret_timeout = False
        result = True

        res, args = agi_send(cmd)[1:]
        dtmf = res

        if res == '-1':
            dtmf = ''
            result = False

        if args[1:-1] == 'timeout':
            ret_timeout = True

        return result, dtmf, ret_timeout
