#!/usr/bin/env python
"""
Run a standard Radar session.
"""

import argparse
import sys
import os
import logging
import logging.config
import json

logger = logging.getLogger(__name__)

def update_python_path():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not root_dir in sys.path:
        sys.path.insert(1, root_dir)

try:
    import cedexis.radar
except ImportError:
    update_python_path()
    import cedexis.radar

def read_config(config_file_path):
    result = {
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

    try:
        with open(config_file_path) as fp:
            result = json.load(fp)
    except TypeError:
        pass

    return result

if __name__ == '__main__':
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
        help= \
            'Your PyRadar API key, available in the Cedexis Portal. This is \
            optional, but if omitted, measurements will not affect Openmix \
            scores or charts',
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
    )

    args = parser.parse_args()

    env_config_file = os.getenv('PYTHON_RADAR_CONFIG')
    config_file_path = os.path.expanduser(env_config_file if args.config_file is None else env_config_file)
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
