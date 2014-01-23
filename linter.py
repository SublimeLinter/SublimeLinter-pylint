#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by NotSqrt
# Copyright (c) 2013 NotSqrt
#
# License: MIT
#

"""This module exports the Pylint plugin class."""

import re
from SublimeLinter.lint import PythonLinter, util


class Pylint(PythonLinter):

    """Provides an interface to pylint."""

    syntax = 'python'
    cmd = (
        'pylint@python',
        '--msg-template=\'{line}:{column}:{msg_id}: {msg}\'',
        '--module-rgx=.*',  # don't check the module name
        '--reports=n',      # remove tables
        '--persistent=n',   # don't save the old score (no sense for temp)
    )
    version_args = '--version'
    version_re = r'^pylint.* (?P<version>\d+\.\d+\.\d+),'
    version_requirement = '>= 1.0'
    regex = (
        r'^(?P<line>\d+):(?P<col>\d+):'
        r'(?P<code>(?:(?P<error>[RFE])|(?P<warning>[CIW]))\d+): '
        r'(?P<message>.*)'
    )
    multiline = True
    line_col_base = (1, 0)
    tempfile_suffix = '.py'
    error_stream = util.STREAM_STDOUT  # ignore missing config file message
    defaults = {
        '--disable=,': '',
        '--enable=,': '',
        '--rcfile=': ''
    }
    inline_overrides = ('enable', 'disable')
    check_version = True

    # a mapping of codes to regexp
    # they are expected to define the 'near' group
    messages_re = {
        'C0102': r'Black listed name "(?P<near>.*)"',
        'C0103': r'Invalid function name "(?P<near>.*)"',
        'C0202': r"Class method (?P<near>.*) should have",
        'C0203': r"Metaclass method (?P<near>.*) should have",
        'C0204': r"Metaclass class method (?P<near>.*) should have",
        'E0001': r'unknown encoding: (?P<near>.*)',
        'E0011': r"Unrecognized file option '(?P<near>.*)'",
        'E0012': r"Bad option value '(?P<near>.*)'",
        'E0108': r"Duplicate argument name (?P<near>.*) in function definition",
        'E0203': r"Access to member '(?P<near>.*)' before its definition",
        'E0603': r"Undefined variable name '(?P<near>.*)' in",
        'E0701': r'Bad except clauses order \(.* is an ancestor class of (?P<near>.*)\)',
        'E0712': r"Catching an exception which doesn't inherit from BaseException: (?P<near>.*)",
        'E1101': r"has no '(?P<near>.*)' member",
        'E1310': r"Suspicious argument in \S+\.(?P<near>.*) call",
        'I0010': r"Unable to consider inline option '(?P<near>.*)'",
        'I0011': r"Locally disabling (?P<near>.*)",
        'I0012': r"Locally enabling (?P<near>.*)",
        'W0102': r'Dangerous default value (?P<near>\S*) (\(.*\) )?as argument',
        'W0106': r'Expression "(?P<near>.*)" is assigned to nothing',
        'W0201': r"Attribute '(?P<near>.*)' defined outside __init__",
        'W0211': r"Static method with '(?P<near>.*)' as first argument",
        'W0212': r"Access to a protected member (?P<near>.*) of a client class",
        'W0402': r"Uses of a deprecated module '(?P<near>.*)'",
        'W0404': r"Reimport '(?P<near>.*)'",
        'W0511': r"(?P<near>.*)",
        'W0512': r'Cannot decode using encoding ".*", unexpected byte at position (?P<col>\d+)',
        'W0611': r"Unused import (?P<near>.*)",
        'W0621': r"Redefining name '(?P<near>.*)' from outer scope",
        'W0622': r"Redefining built-in '(?P<near>.*)'",
        'W0623': r"Redefining name '(?P<near>.*)' from object '.*' in exception handler",
        'W0711': r'Exception to catch is the result of a binary "(?P<near>.*)" operation',
        'W1401': r"Anomalous backslash in string: '(?P<near>.*)'",  # does not work with \o, ...
        'W1402': r"Anomalous Unicode escape in byte string: '(?P<near>.*)'",  # does not work with \u, \U
        'W1501': r'"(?P<near>.*)" is not a valid mode for open',
        'E1124': r"Parameter '(?P<near>.*)' passed as both positional and keyword argument",
        'E1123': r"Passing unexpected keyword argument '(?P<near>.*)' in function call",

        # does not work : 'l' is too short..
        # 'W0332': r'Use of "(?P<near>.*)" as long integer identifier',
    }
    # a static map of codes to 'near' words :
    # some errors always relate to the same keyword.
    messages_near = {
        'C1001': 'class',  # adequately reported at column 0, converted to None
        'W0410': '__future__',  # reported at column 0, converted to None
        'W1201': '%',
        'W0142': '*',
        'W0331': '<>',
        'W0231': '__init__',
        'E0100': '__init__',
        'E0101': '__init__',
        'E1111': '=',
        'W1111': '=',
        'E0106': 'return',
        'W0234': '__iter__',  # or 'next'. TODO find a way to handle both
        'E0711': 'NotImplemented',
        'I0022': '-msg',  # 'disable-msg' or 'enable-msg'. TODO find a way to handle both
        'I0014': 'disable',
        'E0235': '__exit__',
    }

    def split_match(self, match):
        """
        Return the components of the error message.

        We override this to deal with the idiosyncracies of pylint's error messages.

        """

        match, line, col, error, warning, message, near = super().split_match(match)

        if match:
            if col == 0:
                col = None

            code = match.group('code')
            if code in self.messages_near:
                near = self.messages_near[code]
                col = None
            elif code in self.messages_re:
                message_match = re.search(self.messages_re[code], message)
                if message_match:
                    if 'near' in message_match.groupdict():
                        # 'near' will be more precise than 'col'
                        near = message_match.group('near')
                        col = None
                    elif 'col' in message_match.groupdict():
                        col = int(message_match.group('col'))
            elif code == 'C0326':
                if 'assignment' in message:
                    near = '='
                # there are other cases like 'comparison', but it's harder
                # to determine a 'near' value in that case

        return match, line, col, error, warning, message, near
