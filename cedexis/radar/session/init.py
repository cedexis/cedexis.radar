"""
Perform a Radar init request.
"""

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
import datetime
import time
import re

import cedexis.radar
import cedexis.radar.session

def do_init(session_info):
    """Do init request and return request signature"""

    transaction_id = random.randint(1, 999999999)

    try:
        current_time = datetime.datetime.now(datetime.timezone.utc)
        timestamp = int(current_time.timestamp())
    except AttributeError:
        # Python 2
        timestamp = int(time.time())

    domain = 'i1-py-{}-{}-{}-{}-{}-{}.init.cedexis-radar.net'.format(
        cedexis.radar.__sampler_major_version__,
        cedexis.radar.__sampler_minor_version__,
        str(session_info['zone_id']).zfill(2),
        str(session_info['customer_id']).zfill(5),
        transaction_id,
        's' if session_info['secure'] else 'i'
    )

    path = '/i1/{}/{}/jsonp'.format(timestamp, transaction_id)
    cache_buster = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(30))
    parts = (
        'https' if session_info['secure'] else 'http',
        domain,
        path,
        '',
        urlencode({ 'rnd': cache_buster }),
        '',
    )

    url = urlunparse(parts)

    user_agent_string = cedexis.radar.session.make_ua_string(
        session_info['zone_id'],
        session_info['customer_id'],
        session_info['api_key'],
        session_info['tracer']
    )
    request = Request(url, headers={ 'User-Agent': user_agent_string })
    with cedexis.radar.session.closing_urlopen(request, timeout=20) as f:
        response_text = f.read().decode()
    matches = re.search("requestSignature:'([^']+)", response_text)
    return matches.groups()[0]
