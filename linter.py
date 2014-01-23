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


from SublimeLinter.lint import PythonLinter, util


class Pylint(PythonLinter):

    """Provides an interface to pylint."""

    syntax = ('python', 'python django')
    cmd = (
        'pylint@python',
        '--msg-template=\'{line}:{column}:{msg_id}: {msg}\'',
        '--module-rgx=.*',  # don't check the module name
        '--reports=n',      # remove tables
        '--persistent=n',   # don't save the old score (no sense for temp)
    )
    version_args = '--version'
    version_re = r'^pylint (?P<version>\d+\.\d+\.\d+),'
    version_requirement = '>=1.0'
    regex = (
        r'^(?P<line>\d+):(?P<col>\d+):'
        r'(?:(?P<error>[RFE])|(?P<warning>[CIW]))\d+: '
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

    def split_match(self, match):
        """
        Return the components of the error message.

        We override this to deal with the idiosyncracies of pylint's error messages.

        """

        match, line, col, error, warning, message, near = super().split_match(match)

        if match:
            if col == 0:
                col = None

        return match, line, col, error, warning, message, near
