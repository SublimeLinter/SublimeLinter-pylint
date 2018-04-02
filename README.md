SublimeLinter-pylint
=========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-pylint.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-pylint)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [pylint](http://www.pylint.org/).
It will be used with files that have the "python" syntax.


## Installation

SublimeLinter must be installed in order to use this plugin. 

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

Before using this plugin, ensure that `pylint` (1.0 or later) is installed on your system.
To install `pylint`, do the following:

1. Install [Python](http://python.org) and [pip](http://www.pip-installer.org/en/latest/installing.html). If you plan to code in Python 3, you will need to install `pip` for Python 3 as well.

1. Install `pylint` by typing the following in a terminal, replacing ‘x’ with the minor version installed on your system:
   ```bash
   # For python 2.x
   [sudo] pip-2.x install pylint

   # For python 3.x
   [sudo] pip-3.x install pylint

   # On Windows, for python 2.x
   c:\Python2x\Scripts\pip.exe install pylint

   # On Windows, for python 3.x
   c:\Python3x\Scripts\pip.exe install pylint
   ```

Please make sure that the path to `pylint` is available to SublimeLinter.
The docs cover [troubleshooting PATH configuration](http://sublimelinter.com/en/latest/troubleshooting.html#finding-a-linter-executable).


## Settings

- SublimeLinter settings: http://sublimelinter.com/en/latest/settings.html
- Linter settings: http://sublimelinter.com/en/latest/linter_settings.html

Pylint can be configured using `.pylintrc` configuration files and inline comments, more information in [the pylint docs](https://pylint.readthedocs.io/en/latest/faq.html#message-control).
