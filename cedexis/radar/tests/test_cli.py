import unittest
import types

import cedexis.radar.cli

class TestCommandLineInterface(unittest.TestCase):

    def test_main(self):
        self.assertTrue(isinstance(cedexis.radar.cli.main, types.FunctionType))
