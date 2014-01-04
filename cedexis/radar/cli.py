"""
Run a Radar session.
"""

import argparse
import sys
import os
import logging
import logging.config

try:
    FileNotFoundError()
    from cedexis.radar.python3.cli import read_config as read_config_ex
except:
    from cedexis.radar.python2.cli import read_config as read_config_ex

logger = logging.getLogger(__name__)

import cedexis.radar

def read_config(config_file_path):
    default_config = {
        'logging': {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'console_formatter': {
                    'format': '%(name)s (%(levelname)s): %(message)s',
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'console_formatter',
                },
            },
            'root': {
                'level': 'INFO',
                    'handlers': [ 'console', ],
            }
        }
    }
    return read_config_ex(config_file_path, default_config)

def main():
    print(sys.version)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--zone-id',
        '-z',
        type=int,
        default=1,
        help='Your Cedexis Zone ID (defaults to 1)',
    )

    parser.add_argument(
        '--customer-id',
        '-c',
        type=int,
        required=True,
        help='Your Cedexis Customer ID',
    )

    parser.add_argument(
        '--api-key',
        '-k',
        default='sandbox',
        help='reserved',
    )

    parser.add_argument(
        '--secure',
        '-s',
        action='store_true',
    )

    parser.add_argument(
        '--tracer',
        '-t',
        help='An optional tracer to be included in the user agent string',
    )

    parser.add_argument(
        '--provider-id',
        '-p',
        type=int,
        help='Measure a specific provider and quit',
    )

    parser.add_argument(
        '--config-file',
        '-f',
        nargs='?',
        const='',
    )

    args = parser.parse_args()

    env_config_file = os.getenv('CEDEXIS_RADAR_CONFIG')
    config_file_path = os.path.expanduser(env_config_file if args.config_file is None else args.config_file)
    config = read_config(config_file_path)

    # Setup logging
    logging.config.dictConfig(config['logging'])
    logger.debug('Logging configured')
    logger.info('Config file used: %s', config_file_path)
    logger.info('Command line args: %s', args)

    cedexis.radar.run_session(
        args.zone_id,
        args.customer_id,
        args.api_key,
        args.secure,
        args.tracer,
        args.provider_id,
    )
