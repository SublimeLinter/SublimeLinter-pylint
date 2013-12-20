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


from SublimeLinter.lint import Linter


class Pylint(Linter):  # pylint: disable=R0903

    """Provides an interface to pylint."""

    syntax = 'python'
    cmd = (
        'pylint@python',
        '--output-format=parseable',  # easiest format to parse
        '--module-rgx=.*',  # don't check the module name
        '--reports=n',      # remove tables
        '--persistent=n',   # don't save the old score (no sense for temp)
    )
    regex = r'^.*?:(?P<line>\d+): \[(?:(?P<error>[RFE])|(?P<warning>[CIW]))(.*?)\] (?P<message>.*)'
    tempfile_suffix = '.py'
    defaults = {
        '--disable=,': '',
        '--enable=,': '',
        '--rcfile=': ''
    }
    check_version = True
