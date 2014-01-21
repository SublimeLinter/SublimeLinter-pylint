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


from SublimeLinter.lint import PythonLinter


class Pylint(PythonLinter):

    """Provides an interface to pylint."""

    syntax = ('python', 'python django')
    cmd = (
        'pylint@python',
        # '--msg-template={path}:{line}: [{msg_id}({symbol}), {obj}] {msg}',
        # only usable if pylint is >= 1.0
        # so keeping '--output-format=parseable' for now
        '--output-format=parseable',  # easiest format to parse
        '--module-rgx=.*',  # don't check the module name
        '--reports=n',      # remove tables
        '--persistent=n',   # don't save the old score (no sense for temp)
    )
    regex = (
        r'^.*?:(?P<line>\d+): '
        r'\[(?:(?P<error>[RFE])|(?P<warning>[CIW]))(.*?)\] '
        r'(?P<message>.*)'
    )
    tempfile_suffix = '.py'
    defaults = {
        '--disable=,': '',
        '--enable=,': '',
        '--rcfile=': ''
    }
    inline_overrides = ('enable', 'disable')
    check_version = True
