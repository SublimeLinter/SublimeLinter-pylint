import logging
import re
from SublimeLinter.lint import PythonLinter


logger = logging.getLogger('SublimeLinter.plugins.pylint')


class Pylint(PythonLinter):
    regex = (
        r'^(?P<line>\d+):(?P<col>\d+):'
        r'(?P<code>(?:(?P<error>[FE]\d+)|(?P<warning>[CIWR]\d+))): '
        r'(?P<message>.*?)(?:\r?$)'
    )
    multiline = True
    line_col_base = (1, 0)
    tempfile_suffix = '-'
    defaults = {
        # paths to be added to sys.path through --init-hook
        'paths': [],
        'selector': 'source.python',
        '--rcfile=': '',
        '--init-hook=;': None
    }

    def on_stderr(self, stderr):
        stderr = re.sub(
            'No config file found, using default configuration\n', '', stderr)
        stderr = re.sub('Using config file .+\n', '', stderr)
        stderr = re.sub('(?m)^.*DeprecationWarning.*\n.*\n', '', stderr)

        if stderr:
            self.notify_failure()
            logger.error(stderr)

    def cmd(self):
        settings = self.settings
        if settings['init-hook'] is None:
            paths = settings['paths']
            if paths:
                commands = ['import sys'] + [
                    "sys.path.append('{}')".format(path)
                    for path in paths
                ]
                settings['init-hook'] = commands

        return (
            'pylint',
            '--msg-template=\'{line}:{column}:{msg_id}: {msg} ({symbol})\'',
            '--module-rgx=.*',  # don't check the module name
            '--reports=n',      # remove tables
            '--persistent=n',   # don't save the old score (no sense for temp)
            '${args}',
            '${file_on_disk}'
        )

    #############
    # Try to extract a meaningful columns.
    # multiple cases :
    #  - the linter can report a meaningful column
    #  - a 'near' info can be extracted from the message
    #  - the error always refer to the same keyword
    #  - the error concerns the line as a whole
    #  - errors that are confirmed to not be in these cases

    # Errors of type I always report column = 0

    # Already reporting the proper column, use it, even if it is 0
    messages_meaningful_column = [
        'C0321',
        'E0103',
        'E0104',
        'E0105',
        'E0203',
        'E0601',
        'E0602',
        'E0702',
        'E0710',
        'E1004',
        'W0107',
        'W0108',
        'W0110',
        'W0141',
        'W0150',
        'W0233',
        'W0333',
        'W0613',
        'W0631',
        'W0701',
        'W0702',
        'W0703',
        'W0710',
        'W0721',
        'W1001',
    ]

    # a mapping of codes to regexp
    # they are expected to define the 'near' group
    messages_re = {
        'C0102': r'Black listed name "(?P<near>.*)"',
        'C0103': r'Invalid \S+ name "(?P<near>.*)"',
        'C0202': r"Class method (?P<near>.*) should have",
        'C0203': r"Metaclass method (?P<near>.*) should have",
        'C0204': r"Metaclass class method (?P<near>.*) should have",
        'C0301': r"Line too long \(\d+/(?P<col>\d+)\)",
        'C0325': r"Unnecessary parens after '(?P<near>.*)' keyword",
        'E0001': r'unknown encoding: (?P<near>.*)',  # can also be 'invalid syntax', 'EOF in multi-line statement'
        'E0011': r"Unrecognized file option '(?P<near>.*)'",
        'E0012': r"Bad option value '(?P<near>.*)'",
        'E0107': r'Use of the non-existent (?P<near>.*) operator',
        'E0108': r"Duplicate argument name (?P<near>.*) in function definition",
        'E0203': r"Access to member '(?P<near>.*)' before its definition",
        'E0603': r"Undefined variable name '(?P<near>.*)' in",
        'E0604': r"Invalid object '(?P<near>.*)' in",
        'E0611': r"No name '(?P<near>.*)' in module",
        # may also be: Bad except clauses order (empty except clause should always appear last)
        # which is reported on the 'try'  -> keep the column info !
        'E0701': r'Bad except clauses order \(.* is an ancestor class of (?P<near>.*)\)',
        'E0712': r"Catching an exception which doesn't inherit from BaseException: (?P<near>.*)",
        'E1003': r"Bad first argument '(?P<near>.*)' given to super()",
        'E1101': r"has no '(?P<near>.*)' member",
        'E1102': r"(?P<near>.*) is not callable",
        'E1103': r"has no '(?P<near>.*)' member",
        'E1123': r"Passing unexpected keyword argument '(?P<near>.*)' in function call",
        'E1124': r"Parameter '(?P<near>.*)' passed as both positional and keyword argument",
        'E1310': r"Suspicious argument in \S+\.(?P<near>.*) call",
        'F0220': r"failed to resolve interfaces implemented by \S+ \((?P<near>.*)\)",
        'F0401': r"Unable to import '(?P<near>.*)'",
        'I0010': r"Unable to consider inline option '(?P<near>.*)'",
        'I0011': r"Locally disabling (?P<near>.*)",
        'I0012': r"Locally enabling (?P<near>.*)",
        'W0102': r'Dangerous default value (?P<near>\S*) (\(.*\) )?as argument',
        'W0106': r'Expression "\((?P<near>.*)\)" is assigned to nothing',  # FIXME regex too greedy ?
        'W0201': r"Attribute '(?P<near>.*)' defined outside __init__",
        'W0211': r"Static method with '(?P<near>.*)' as first argument",
        'W0212': r"Access to a protected member (?P<near>.*) of a client class",
        'W0402': r"Uses of a deprecated module '(?P<near>.*)'",
        'W0403': r"Relative import '(?P<near>.*)', should be",
        'W0404': r"Reimport '(?P<near>.*)'",
        'W0511': r"(?P<near>.*)",
        'W0512': r'Cannot decode using encoding ".*", unexpected byte at position (?P<col>\d+)',
        'W0601': r"Global variable '(?P<near>.*)' undefined",
        'W0602': r"Using global for '(?P<near>.*)' but",
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
        'E0106': 'return',
        'E0235': '__exit__',
        'E0711': 'NotImplemented',
        'E1111': '=',
        'I0014': 'disable',
        'I0022': '-msg',  # 'disable-msg' or 'enable-msg'. TODO find a way to highlight both
        'W0122': 'exec',
        'W0142': '*',
        'W0231': '__init__',
        'W0234': '__iter__',  # or 'next'. TODO find a way to handle both
        'W0301': ';',
        'W0331': '<>',
        'W0401': 'import *',
        'W0410': '__future__',  # reported at column 0, converted to None
        'W0603': 'global',
        'W0604': 'global',
        'W0614': 'import *',
        'W1111': '=',
        'W1201': '%',
    }

    # Could not be generated:
    # C0121, C0303, C0304,
    # E0604,
    # F0002, F0003, F0004, F0010, F0202,
    # I0001, I0020, I0021,
    # W0232, W0404, W0704

    # Confirmed to not report a meaningful column, and to not allow for 'near' extraction
    # They are typically about a whole class or method.
    # These will be forced to None.
    messages_no_column = [
        'C0111',  # mssing docstring for modules, classes and methods
        'C0112',  # empty docstring for modules, classes and methods
        'C0302',
        'C0303',
        'C0304',
        # 'C0326',  # special case TODO find a way to use the next 2 lines on
        # the report, which shows the position of the error.
        'C1001',
        'E0001',
        'E0102',
        'E0202',
        'E0211',
        'E0213',
        'E0221',
        'E0222',
        'E1001',
        'E1002',
        'E1120',
        'E1121',
        'E1125',
        'E1200',
        'E1201',
        'E1205',
        'E1206',
        'E1300',
        'E1301',
        'E1302',
        'E1303',
        'E1304',
        'E1305',
        'E1306',
        'I0013',
        'R0902',
        'R0903',
        'R0911',
        'R0912',
        'R0914',
        'W0101',
        'W0104',
        'W0105',
        'W0109',  # on a multiline dict, it is reported on the assignment line
        'W0120',
        'W0121',
        'W0199',
        'W0221',
        'W0222',
        'W0223',
        'W0232',
        'W0311',
        'W0312',
        'W0406',
        'W0632',
        'W0633',
        'W0712',
        'W1300',
        'W1301',
    ]

    def split_match(self, match):
        """
        Return the components of the error message.

        We override this to deal with the idiosyncracies of pylint's error messages.
        """
        match, line, col, error, warning, message, near = super().split_match(match)

        if match:
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
                # else: keeping the column info anyway, useful for E0701
            elif code == 'C0326':
                if 'assignment' in message:
                    near = '='
                # there are other cases like 'comparison', but it's harder
                # to determine a 'near' value in that case
            elif code in self.messages_no_column:
                col = None
            else:
                # if it is an unknown error code, force it if column = 0
                if col == 0:
                    col = None

        return match, line, col, error, warning, message, near
