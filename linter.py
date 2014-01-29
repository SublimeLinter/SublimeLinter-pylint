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
        'C0103': r'Invalid \S+ name "(?P<near>.*)"',
        'C0202': r"Class method (?P<near>.*) should have",
        'C0203': r"Metaclass method (?P<near>.*) should have",
        'C0204': r"Metaclass class method (?P<near>.*) should have",
        'E0001': r'unknown encoding: (?P<near>.*)',  # can also be 'invalid syntax', 'EOF in multi-line statement'
        'E0011': r"Unrecognized file option '(?P<near>.*)'",
        'E0012': r"Bad option value '(?P<near>.*)'",
        'E0108': r"Duplicate argument name (?P<near>.*) in function definition",
        'E0203': r"Access to member '(?P<near>.*)' before its definition",
        # 'E0601': r"Using variable '(?P<near>.*)' before assignment",
        # 'E0602': r"Undefined variable '(?P<near>.*)'",
        # 'E0603': r"Undefined variable name '(?P<near>.*)' in",
        'E0611': r"No name '(?P<near>.*)' in module",
        'E0701': r'Bad except clauses order \(.* is an ancestor class of (?P<near>.*)\)',  # may also be Bad except clauses order (empty except clause should always appear last)
        'E0712': r"Catching an exception which doesn't inherit from BaseException: (?P<near>.*)",
        'E1003': r"Bad first argument '(?P<near>.*)' given to super()",
        'E1101': r"has no '(?P<near>.*)' member",
        'E1102': r"(?P<near>.*) is not callable",
        'E1123': r"Passing unexpected keyword argument '(?P<near>.*)' in function call",
        'E1124': r"Parameter '(?P<near>.*)' passed as both positional and keyword argument",
        'E1310': r"Suspicious argument in \S+\.(?P<near>.*) call",
        'F0401': r"Unable to import '(?P<near>.*)'",
        'I0010': r"Unable to consider inline option '(?P<near>.*)'",
        'I0011': r"Locally disabling (?P<near>.*)",
        'I0012': r"Locally enabling (?P<near>.*)",
        'W0102': r'Dangerous default value (?P<near>\S*) (\(.*\) )?as argument',
        'W0106': r'Expression "(?P<near>.*)" is assigned to nothing',
        'W0201': r"Attribute '(?P<near>.*)' defined outside __init__",
        'W0211': r"Static method with '(?P<near>.*)' as first argument",
        'W0212': r"Access to a protected member (?P<near>.*) of a client class",
        'W0402': r"Uses of a deprecated module '(?P<near>.*)'",
        'W0403': r"Relative import '(?P<near>.*)', should be",
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

        # does not work : 'l' is too short..
        # 'W0332': r'Use of "(?P<near>.*)" as long integer identifier',
    }
    # a static map of codes to 'near' words :
    # some errors always relate to the same keyword.
    messages_near = {
        'C1001': 'class',  # adequately reported at column 0, converted to None
        'E0100': '__init__',
        'E0101': '__init__',
        'E0104': 'return',
        'E0105': 'yield',
        'E0106': 'return',
        'E0235': '__exit__',
        'E0711': 'NotImplemented',
        'E1111': '=',
        'I0014': 'disable',
        'I0022': '-msg',  # 'disable-msg' or 'enable-msg'. TODO find a way to handle both
        'W0122': 'exec',
        'W0142': '*',
        'W0231': '__init__',
        'W0234': '__iter__',  # or 'next'. TODO find a way to handle both
        'W0301': ';',
        'W0331': '<>',
        'W0410': '__future__',  # reported at column 0, converted to None
        'W1111': '=',
        'W1201': '%',
    }

    # already report the proper column:
    # E0601, E0602, E0603, E1004

    # TODO
    # C0112, C0321, C0325, E0102, E0103, E0107, E0202, E0211, E0213, E0221, E0604
    # E0702, E0710, E1120

    # confirmed to not report a column, and to not allow for 'near' extraction
    messages_no_column = [
        'C0111',
        'C0112',
        'C0301',
        'C0302',
        'C0303',
        'C0304',
        # 'C0326',  # special case
        'C1001',
        'E0001',
        'E0222',
        'E1001',
        'E1002',
        'E1121',
        'E1125',
        'I0013',
        'R0902',
        'R0903',
        'R0911',
        'R0912',
        'R0914',
        'W0104',
        'W0105',
        'W0199',
        'W0232',
        'W0312',
    ]

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
