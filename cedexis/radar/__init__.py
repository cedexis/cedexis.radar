try:
    from urllib.error import URLError as url_error
except ImportError:
    # Python 2
    from urllib2 import URLError as url_error

import random
import logging

logger = logging.getLogger(__name__)

"""
Fields:
- version
- zone id
- customer id
- API key
- optional tracer
"""

import cedexis.radar.session.init
import cedexis.radar.session.probeserver
# import cedexis.radar.session.measure
# import cedexis.radar.session.report

__sampler_major_version__ = 0
__sampler_minor_version__ = 2
__sampler_micro_version__ = 0
__version_suffix__ = ''

def run_session(zone_id, customer_id, api_key='sandbox', secure=False, tracer=None, provider_id=None, strict=False, report_server='reports.cedexis.com'):
    """Run a Radar session"""
    session_info = {
        'zone_id': zone_id,
        'customer_id': customer_id,
        'api_key': api_key,
        'secure': secure,
        'tracer': tracer,
        'strict': False,
        'report_server': report_server,
        'transaction_id': random.randint(1, 999999999)
    }

    providers_measured = 0
    try:
        session_info['request_signature'] = cedexis.radar.session.init.do_init(session_info)
        logger.debug('Request signature: %s', session_info['request_signature'])
        logger.debug('Transaction id: %s', session_info['transaction_id'])
        providers = cedexis.radar.session.probeserver.get_providers(session_info, provider_id)
        for provider in providers:
            provider.measure()
            providers_measured += 1

    # except (url_error, Exception) as e:
    #     logger.error('Error in session; %s', e)
    finally:
        logger.info('%s providers measured', providers_measured)
