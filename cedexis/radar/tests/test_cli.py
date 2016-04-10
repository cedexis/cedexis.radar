import unittest
from unittest.mock import patch, MagicMock, call
import types
from pprint import pprint

import cedexis.radar.cli

class TestCommandLineInterface(unittest.TestCase):

    def test_main(self):
        self.assertTrue(isinstance(cedexis.radar.cli.main, types.FunctionType))

    @patch('logging.getLogger')
    @patch('argparse.ArgumentParser')
    @patch('cedexis.radar.run_session')
    @patch('time.sleep')
    def test_config_file_with_cli_params(self, mock_sleep, mock_run_session,
        mock_ArgumentParser, mock_getLogger):
        args = make_default_args()
        args.continuous = True
        args.max_runs = 3
        args.repeat_delay = 60
        mock_parser = MagicMock()
        mock_parser.parse_args.return_value = args
        mock_ArgumentParser.return_value = mock_parser
        cedexis.radar.cli.main()

        # Assert
        # print(mock_run_session.call_args)
        self.assertEqual(
            mock_run_session.call_args_list,
            [
                call(1, 12345, 'sandbox', False, None, None, False, None),
                call(1, 12345, 'sandbox', False, None, None, False, None),
                call(1, 12345, 'sandbox', False, None, None, False, None)
            ])
        # print(mock_sleep.call_args)
        self.assertEqual(mock_sleep.call_args_list, [call(60),call(60)])

def make_default_args():
    args = lambda: None
    args.zone_id = 1
    args.customer_id = 12345
    args.api_key = 'sandbox'
    args.secure = False
    args.config_file = 'some config file path'
    args.tracer = None
    args.provider_id = None
    args.report_server = None
    args.max_runs = None
    args.repeat_delay = None
    return args
