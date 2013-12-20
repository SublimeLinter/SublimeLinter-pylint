SublimeLinter-pylint
=========================

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter3) provides an interface to [pylint](http://www.pylint.org/). It will be used with files that have the “python” syntax.

## Installation
SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter 3 is not installed, please follow the instructions [here](https://github.com/SublimeLinter/SublimeLinter.github.io/wiki/Installation).

### Linter installation
Before using this plugin, you must ensure that `pylint` is installed on your system. To install `pylint`, do the following:

1. Install Python.

1. Install `pylint` by typing the following in a terminal:
   ```
   pip install pylint
   ```

Once pylint is installed, you can proceed to install the SublimeLinter-pylint plugin if it is not yet installed.

### Plugin installation
Please use [Package Control](https://sublime.wbond.net/installation) to install the linter plugin. This will ensure that the plugin will be updated when new versions are available. If you want to install from source so you can modify the source code, you probably know what you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette](http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html) and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `pylint`. Among the entries you should see `SublimeLinter-pylint`. If that entry is not highlighted, use the keyboard or mouse to select it.

## Settings
For general information on how SublimeLinter works with settings, please see [Settings](https://github.com/SublimeLinter/SublimeLinter.github.io/wiki/Settings). For information on generic linter settings, please see [Linter Settings](https://github.com/SublimeLinter/SublimeLinter.github.io/wiki/Linter-Settings).

In addition to the standard SublimeLinter settings, SublimeLinter-pylint provides its own settings. Those marked as “Inline Setting” or “Inline Override” may also be [used inline](https://github.com/SublimeLinter/SublimeLinter.github.io/wiki/Settings#inline-settings).

|Setting|Description|Inline Setting|Inline Override|
|:------|:----------|:------------:|:-------------:|
|disable| Disable the message, report, category or checker with the given comma-separated id(s)| | |
|enable| Enable the message, report, category or checker with the given comma-separated id(s)| | |
|rcfile| Absolute path to a pylint configuration file| | |

## Notes on Pylint and errors

Remember that you can locally disable errors by putting a comment similar to ``  # pylint: disable=R0903`` at the end of the incriminated lines. 
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

Thank you for helping out!
