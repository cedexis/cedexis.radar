
try:
    from urllib.parse import urlencode, urlunparse
    from urllib.request import Request
except ImportError:
    # Python 2
    from urlparse import urlunparse
    from urllib import urlencode
    from urllib2 import Request

import random
import string
import json
import sys
import logging
from datetime import datetime
import calendar
from pprint import pprint

logger = logging.getLogger(__name__)

import cedexis.radar.session
import cedexis.radar.provider

def get_providers(session_info, provider_id):
    pprint(session_info)
    domain = 'radar.cedexis.com'
    provider_ids = []

    now = datetime.utcnow();
    ts = calendar.timegm(now.utctimetuple())

    query_string_parts = {
        'imagesok': '1',
        't': '1'
    }
    if not provider_id is None:
        query_string_parts['providersSet'] = provider_id
    elif 0 < len(provider_ids):
        query_string_parts['providersSet'] = ','.join(provider_ids)

    query_string = urlencode(query_string_parts)
    path = '/{}/{}/radar/{}/{}/providers.json'.format(
        session_info['zone_id'],
        session_info['customer_id'],
        ts,
        ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))
    )

    parts = (
        'https' if session_info['secure'] else 'http',
        domain,
        path,
        '',
        query_string,
        '',
    )

    url = urlunparse(parts)
    logger.debug('providers.json URL: %s', url)

    user_agent_string = cedexis.radar.session.make_ua_string(
        session_info['zone_id'],
        session_info['customer_id'],
        session_info['tracer'],
    )
    request = Request(url, headers={ 'User-Agent': user_agent_string })
    with cedexis.radar.session.closing_urlopen(request) as f:
        try:
            response_text = f.read().decode()
        except Exception as e:
            logger.error('providers.json communication error: %s', e)
            return

    logger.debug('providers.json content: %s', response_text)
    result = []
    for i in json.loads(response_text):
        provider = cedexis.radar.provider.Provider(
            i,
            session_info['zone_id'],
            session_info['customer_id'],
            session_info['transaction_id'],
            session_info['request_signature'],
            session_info['tracer'],
            session_info['secure'],
            session_info['report_server']
        )
        result.append(provider)
    return result
