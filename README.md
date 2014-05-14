SublimeLinter-pylint
=========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-pylint.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-pylint)

This linter plugin for [SublimeLinter][docs] provides an interface to [pylint](http://www.pylint.org/). It will be used with files that have the “python” syntax.

## Installation
SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter 3 is not installed, please follow the instructions [here][installation].

### Linter installation
Before using this plugin, you must ensure that `pylint` is installed on your system. To install `pylint`, do the following:

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

**Note:** This plugin requires `pylint` 1.0 or later.

### Linter configuration
In order for `pylint` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. Before going any further, please read and follow the steps in [“Finding a linter executable”](http://sublimelinter.readthedocs.org/en/latest/troubleshooting.html#finding-a-linter-executable) through “Validating your PATH” in the documentation.

Once you have installed and configured `pylint`, you can proceed to install the SublimeLinter-pylint plugin if it is not yet installed.

### Plugin installation
Please use [Package Control][pc] to install the linter plugin. This will ensure that the plugin will be updated when new versions are available. If you want to install from source so you can modify the source code, you probably know what you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette][cmd] and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `pylint`. Among the entries you should see `SublimeLinter-pylint`. If that entry is not highlighted, use the keyboard or mouse to select it.

## Settings
For general information on how SublimeLinter works with settings, please see [Settings][settings]. For information on generic linter settings, please see [Linter Settings][linter-settings].

In addition to the standard SublimeLinter settings, SublimeLinter-pylint provides its own settings. Those marked as “Inline Setting” or “Inline Override” may also be [used inline][inline-settings].

|Setting|Description|Inline Setting|Inline Override|
|:------|:----------|:------------:|:-------------:|
|@python|A meta setting that indicates the [python version][python-version] of your source files. Use this inline or at the global level, not within the linter’s settings.|&#10003;| |
|disable| Disable the message, report, category or checker with the given comma-separated id(s)| |&#10003;|
|enable| Enable the message, report, category or checker with the given comma-separated id(s)| |&#10003;|
|rcfile| Absolute path to a pylint configuration file| | |
|paths| A list of paths to be added to sys.path for pylint to find modules| | |
|show-codes| Boolean that indicates whether you want the pylint code to be displayed in the status bar| | |

## Notes on Pylint and errors

Remember that you can locally disable errors by putting a comment similar to ``  # pylint: disable=R0903`` at the end of the offending lines.
By doing so, you will generate a new error called ``I0011``, that you may want to globally ignore through your settings.

## Contributing
If you would like to contribute enhancements or fixes, please do the following:

1. Fork the plugin repository.
1. Hack on a separate topic branch created from the latest `master`.
1. Commit and push the topic branch.
1. Make a pull request.
1. Be patient.  ;-)

Please note that modications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Vertical whitespace helps readability, don’t be afraid to use it.
- Please use descriptive variable names, no abbrevations unless they are very well known.

Thank you for helping out!

[docs]: http://sublimelinter.readthedocs.org
[installation]: http://sublimelinter.readthedocs.org/en/latest/installation.html
[locating-executables]: http://sublimelinter.readthedocs.org/en/latest/usage.html#how-linter-executables-are-located
[python-version]: http://sublimelinter.readthedocs.org/en/latest/meta_settings.html#python
[pc]: https://sublime.wbond.net/installation
[cmd]: http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html
[settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html
[linter-settings]: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html
[inline-settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html#inline-settings
