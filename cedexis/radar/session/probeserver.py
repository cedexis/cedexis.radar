
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

logger = logging.getLogger(__name__)

import cedexis.radar.session

def reorder_for_uni(probes):
    new_list = []
    for i in probes:
        if 'uni' != i['a']:
            new_list.append(i)
        else:
            new_list.insert(0, i)
    return new_list

def get_providers(session_info, provider_id):

    domain = 'probes.cedexis.com'
    provider_ids = []

    while True:
        parts = {
            'z': session_info['zone_id'],
            'c': session_info['customer_id'],
            'fmt': 'json',
            'rnd': ''.join(random.choice(string.ascii_letters + string.digits) for i in range(30))
        }

        if not provider_id is None:
            parts['pid'] = provider_id
        elif 0 < len(provider_ids):
            parts['i'] = ','.join(provider_ids)

        query_string = urlencode(parts)

        parts = (
            'https' if session_info['secure'] else 'http',
            domain,
            '',
            '',
            query_string,
            '',
        )

        url = urlunparse(parts)
        logger.debug('Probeserer URL: %s', url)

        user_agent_string = cedexis.radar.session.make_ua_string(
            session_info['zone_id'],
            session_info['customer_id'],
            session_info['api_key'],
            session_info['tracer'],
        )
        request = Request(url, headers={ 'User-Agent': user_agent_string })
        with cedexis.radar.session.closing_urlopen(request) as f:
            try:
                response_text = f.read().decode()
            except Exception as e:
                logger.error('Error communicating with ProbeServer: %s', e)
                return

        logger.debug('Probeserver response: %s', response_text)
        try:
            json_result = json.loads(response_text)
            json_result['p']['p'] = reorder_for_uni(json_result['p']['p'])
            provider_ids.append(str(json_result['p']['i']))
            yield json_result
        except KeyError:
            return
        except ValueError as e:
            logger.info('Error from Probeserver: {}'.format(e))
            return

        if not provider_id is None:
            return
