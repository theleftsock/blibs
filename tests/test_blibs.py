#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `blibs` package."""


import unittest
from click.testing import CliRunner

import blibs.foreman as fm

class TestBlibs(unittest.TestCase):
    """Tests for `blibs` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'blibs.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output


if __name__ == "__main__":
    print("hello_world")
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    fm.get_list_dir(dir_path)
