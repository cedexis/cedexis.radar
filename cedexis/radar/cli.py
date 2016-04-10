"""
Run a Radar session.
"""

import argparse
import sys
import os
import logging
import logging.config

def update_python_path():
    source_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(1, source_dir)

try:
    try:
        FileNotFoundError()
        from cedexis.radar.python3.cli import read_config as read_config_ex
    except:
        from cedexis.radar.python2.cli import read_config as read_config_ex
except ImportError:
    update_python_path()
    # ...and try again
    try:
        FileNotFoundError()
        from cedexis.radar.python3.cli import read_config as read_config_ex
    except:
        from cedexis.radar.python2.cli import read_config as read_config_ex

logger = logging.getLogger(__name__)

import cedexis.radar
import cedexis.radar._crlogging

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

    if config_file_path is None:
        return default_config

    return read_config_ex(config_file_path, default_config)

def main():
    print(sys.version)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--zone-id',
        '-z',
        type=int,
        help='Your Cedexis Zone ID',
    )

    parser.add_argument(
        '--customer-id',
        '-c',
        type=int,
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

    parser.add_argument(
        '--report-server',
        '-r',
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
    )

    args = parser.parse_args()

    env_config_file = os.getenv('CEDEXIS_RADAR_CONFIG')
    config_file_path = None
    uses_default_config = False
    if not env_config_file is None:
        config_file_path = os.path.expanduser(env_config_file)
    elif not args.config_file is None:
        config_file_path = os.path.expanduser(args.config_file)
    else:
        uses_default_config = True
    config = read_config(config_file_path)
    if uses_default_config and args.verbose:
        config['logging']['handlers']['console']['level'] = 'DEBUG'
        config['logging']['root']['level'] = 'DEBUG'

    # Setup logging
    logging.config.dictConfig(config['logging'])
    logger.debug('Logging configured')
    logger.info('Config file used: %s', config_file_path)
    logger.info('Command line args: %s', args)

    # Sensible defaults
    zone_id = 1
    customer_id = None

    # Default zone and customer ids to what's in the config file but
    # allow the command line arguments to override them
    try:
        zone_id = config['customer']['zone_id']
        customer_id = config['customer']['customer_id']
    except KeyError:
        pass

    if not args.zone_id is None:
        zone_id = args.zone_id
    if not args.customer_id is None:
        customer_id = args.customer_id
    if zone_id is None or customer_id is None:
        raise Exception('Zone and customer id must be specified either in the'
            ' config file or using the --zone-id/-z and --customer-id/-c'
            ' command line arguments.')

    cedexis.radar.run_session(
        zone_id,
        customer_id,
        args.api_key,
        args.secure,
        args.tracer,
        args.provider_id,
        False,
        args.report_server,
    )

if __name__ == '__main__':
    main()
