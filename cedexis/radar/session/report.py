
try:
    from urllib.parse import urlencode, urlunparse
    from urllib.request import Request
    from urllib.error import URLError as url_error
except ImportError:
    # Python 2
    from urlparse import urlunparse
    from urllib import urlencode
    from urllib2 import Request, URLError as url_error

import random
import string
import logging

logger = logging.getLogger(__name__)

import cedexis.radar.session
import cedexis.radar.session.errors

def send_reports(session_info, data):
    """Send reports"""

    def make_url():

        path_parts = [
            'f1',
            session_info['request_signature'],
            str(report['p_o_zid']),
            str(report['p_o_cid']),
            str(report['pid']),
            str(report['probe_id']),
        ]

        if 'timeout' == report['status']:
            path_parts.append('1')
        elif 'error' == report['status']:
            path_parts.append('4')
        elif 'success' == report['status']:
            path_parts.append('0')
        else:
            raise cedexis.radar.session.errors.UnexpectedStatusError()

        path_parts.append(str(report['measurement']))
        path_parts.append(report['uni'])
        path_parts.append('1') # No support for partner tags

        query_string = urlencode({
            'rnd': ''.join(random.choice(string.ascii_letters + string.digits) for i in range(30))
        })

        parts = (
            'https' if session_info['secure'] else 'http',
            'reports.cedexis.com' if session_info['report_server'] is None else session_info['report_server'],
            '/'.join(path_parts),
            '',
            query_string,
            ''
        )
        return urlunparse(parts)

    def make_request():
        url = make_url()
        logger.debug('Report: %s', url)
        user_agent_string = cedexis.radar.session.make_ua_string(
            session_info['zone_id'],
            session_info['customer_id'],
            session_info['api_key'],
            session_info['tracer'],
        )
        logger.debug('User agent: %s', user_agent_string)
        return Request(url, headers={ 'User-Agent': user_agent_string })

    for report in data:
        request = make_request()
        with cedexis.radar.session.closing_urlopen(request, timeout=20) as f:
            try:
                f.read()
            except url_error as e:
                logger.warning('Error sending report: %s', e)
            except IOError as e:
                logger.warning('Error sending report: %s', e)
