import importlib
import unittest

import sublime


LinterModule = importlib.import_module('SublimeLinter-pylint.linter')
Linter = LinterModule.Pylint


class TestNear(unittest.TestCase):
    def assertMatch(self, string, expected):
        linter = Linter(sublime.View(0), {})
        actual = list(linter.find_errors(string))[0]
        # `find_errors` fills out more information we don't want to write down
        # in the examples
        self.assertEqual({k: actual[k] for k in expected.keys()}, expected)

    def test_unused_import(self):
        # `--msg-template` appends ` ({symbol})`; it must not end up in `near`
        self.assertMatch(
            "1:0:W0611: Unused import os (unused-import)",
            {'line': 0, 'near': 'os', 'col': None},
        )
        self.assertMatch(
            "3:0:W0611: Unused import os.path (unused-import)",
            {'line': 2, 'near': 'os.path'},
        )

    def test_fixme(self):
        self.assertMatch(
            "6:1:W0511: TODO: fix this (fixme)",
            {'line': 5, 'near': 'TODO: fix this', 'col': None},
        )

    def test_message_keeps_the_symbol(self):
        self.assertMatch(
            "1:0:W0611: Unused import os (unused-import)",
            {'message': 'Unused import os (unused-import)'},
        )

    def test_other_near_patterns_still_work(self):
        self.assertMatch(
            "7:10:E0602: Undefined variable 'undefined_name' (undefined-variable)",
            {'line': 6, 'col': 10},
        )
        self.assertMatch(
            "5:0:W0102: Dangerous default value [] as argument (dangerous-default-value)",
            {'near': '[]'},
        )
        self.assertMatch(
            "13:8:W0201: Attribute 'y' defined outside __init__ (attribute-defined-outside-init)",
            {'near': 'y'},
        )
        self.assertMatch(
            "2:0:E0611: No name 'foo' in module 'bar' (no-name-in-module)",
            {'near': 'foo'},
        )
