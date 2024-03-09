#!/usr/bin/python3
"""Tests for the products console"""
import unittest


import console


class TestConsole(unittest.TestCase):

    """Tests for the products console"""

    def test_quit(self):
        """Ensures that the user can exit the console"""

        self.assertTrue(console.Console().onecmd("EOF"))
        self.assertTrue(console.Console().onecmd("quit"))


if __name__ == "__main__":
    unittest.main()
