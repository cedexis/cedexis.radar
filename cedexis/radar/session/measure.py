
try:
    from urllib.parse import urlencode, urlunparse, urlparse, parse_qsl
    from urllib.request import Request
    from urllib.error import URLError as url_error
except ImportError:
    # Python 2
    from urlparse import urlunparse, urlparse, parse_qsl
    from urllib import urlencode
    from urllib2 import Request, URLError as url_error

import socket
import random
import string
import sys
import time
import logging
import json
from pprint import pformat
import re
import contextlib

logger = logging.getLogger(__name__)

import cedexis.radar.session
import cedexis.radar.session.errors
import cedexis.radar.session.uni

class Probe(object):

    def __init__(self, provider_data, spec):
        self.__provider = provider_data
        self.__spec = spec

    @property
    def is_cold(self):
        return self.__spec['t'] in [ 1, 11 ]

    @property
    def is_throughput(self):
        return self.__spec['t'] in [ 14, 15 ]

    @property
    def is_uni_ajax(self):
        return 'uni' == self.__spec['a'] and 'ajax' == self.__spec['v']

    @property
    def is_uni_jsonp(self):
        return 'uni' == self.__spec['a'] and 'jsonp' == self.__spec['v']

    def get_cache_buster(self):
        if self.__provider['cache_busting']:
            return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(30))
        return None

    def make_query_string(self, existing):
        qs_data = parse_qsl(existing)
        cache_buster = self.get_cache_buster()
        if not cache_buster is None:
            qs_data.append(( 'rnd', cache_buster, ))
        return urlencode(qs_data)

    def make_url(self):
        """Do measurement and return report data"""
        parts = urlparse(self.__spec['u'])
        query_string = self.make_query_string(parts.query)
        parts = (
            parts.scheme,
            parts.netloc,
            parts.path,
            parts.params,
            query_string,
            parts.fragment
        )
        return urlunparse(parts)

    def make_request(self, session_info, request_headers=None):
        url = self.make_url()
        logger.debug('Probe URL: %s', url)
        user_agent_string = cedexis.radar.session.make_ua_string(
            session_info['zone_id'],
            session_info['customer_id'],
            session_info['api_key'],
            session_info['tracer'],
        )
        headers = { 'User-Agent': user_agent_string }
        if not request_headers is None:
            headers.update(request_headers)
        return Request(url, headers=headers)

    def measure(self, session_info):
        """Do measurement and return report data"""
        #request = self.make_request(session_info)
        result = {
            'p_o_zid': self.__provider['p_o_zid'],
            'p_o_cid': self.__provider['p_o_cid'],
            'pid': self.__provider['pid'],
            'probe_id': self.__spec['t'],
            'status': 'success',
            'uni': self.__provider['uni'],
            'measurement': 0,
        }
        buffer_size = 1024

        try:
            stopwatch = time.perf_counter
        except AttributeError:
            # Python 2
            stopwatch = time.time

        # Setup initial request
        current_probe_url = self.make_url()
        logger.debug('Current URL: %s', current_probe_url)
        probe_url_parts = urlparse(current_probe_url)
        logger.debug('Probe URL parts: %s', probe_url_parts)
        probe_ip = socket.gethostbyname(probe_url_parts.netloc)
        logger.debug('Probe IP: %s', probe_ip)
        query_string = ''
        if 0 < len(probe_url_parts.query):
            query_string = '?' + probe_url_parts.query
        message = 'GET {}{} HTTP/1.0\r\nHost: {}\r\n\r\n'.format(
            probe_url_parts.path,
            query_string,
            probe_url_parts.netloc
        )
        logger.debug('Message: %s', message)
        logger.debug('Message type: %s', type(message))

        try:
            if self.is_cold:
                # Start timer for cold probe
                start = stopwatch()

            # Make initial connection
            with contextlib.closing(socket.create_connection((probe_url_parts.netloc, 80), timeout=7)) as s:
                if not self.is_cold:
                    # Start timer for non-cold probe
                    start = stopwatch()

                # Send message
                s.send(message.encode('utf-8'))
                response_parts = []

                # Get response
                while True:
                    data = s.recv(buffer_size)
                    if not data:
                        break
                    response_parts.append(data)

                re_status = b'HTTP/\d\.\d\s(\d+)\s([\w ]+)'
                ok = b'200'
                found = b'302'
                see_other = b'303'
                temp_redirect = b'307'
                try:
                    response_text = b''.join(response_parts)
                except TypeError:
                    # Deal with str
                    re_status = 'HTTP/\d\.\d\s(\d+)\s([\w ]+)'
                    ok = '200'
                    found = '302'
                    see_other = '303'
                    temp_redirect = '307'
                    response_text = ''.join(response_parts)

                match = re.search(re_status, response_text)
                logger.debug('match: %s', match.groups())
                if ok == match.group(1):
                    elapsed = int(1000 * (stopwatch() - start))
                    logger.debug('Time elapsed: %s', elapsed)
                elif not match.group(1) in [ found, see_other, temp_redirect ]:
                    raise session.errors.UnexpectedHttpStatusError(
                        int(match.group(1)), match.group(2).decode('utf-8'))
                else:
                    # Fall back to urllib to handle redirect (should be rare)
                    request = self.make_request(session_info)
                    try:
                        # Start timer
                        start = stopwatch()
                        with cedexis.radar.session.closing_urlopen(request, timeout=7) as f:
                            response_text = f.read()
                            # Get elapsed time in milliseconds
                            elapsed = int(1000 * (stopwatch() - start))
                        logger.debug('Time elapsed: %s', elapsed)
                    except url_error:
                        result['status'] = 'error'

                logger.debug('Probe response text length: %s', len(response_text))
                #logger.debug('Probe response text: %s', response_text.decode('utf-8'))
                if 'success' == result['status']:
                    if 6000 <= elapsed:
                        result['status'] = 'timeout'
                    else:
                        result['measurement'] = self.calculate_throughput(elapsed) if self.is_throughput else elapsed
        except socket.timeout:
            result['status'] = 'error'

        if 'success' != result['status']:
            # Stop processing this provider
            self.__provider['continue'] = False

        return result

    def calculate_throughput(self, elapsed):
        if 0 == self.__spec['s']:
            raise session.errors.InvalidThroughputFileSizeError()
        result = 8 * 1000 * self.__spec['s'] // elapsed
        return result

    def get_uni_ajax(self, session_info):
        """Return 1 unless we can get the uni for this provider"""
        try:
            uni_reader = cedexis.radar.session.uni.providers[self.__provider['pid']]
            request = self.make_request(session_info, uni_reader.request_headers)
            with cedexis.radar.session.closing_urlopen(request) as response:
                try:
                    headers = response.getheaders()
                except AttributeError:
                    # Python 2
                    headers = [ (i[0], i[1]) for i in [ i.split(': ') for i in [ i.strip() for i in response.info().headers ] ] ]
        except url_error as e:
            logger.warning('Encountered error getting UNI for pid %s; %s', self.__provider['pid'], e)
            self.__provider['uni'] = '2'
            return
        except KeyError:
            logger.warning('UNI for pid %s not handled', self.__provider['pid'])
            if not session_info['strict']:
                self.__provider['uni'] = '0'
                return
            else:
                raise
        logger.debug('UNI request headers: %s', pformat(headers))
        self.__provider['uni'] = uni_reader.uni_from_headers(headers)

    def get_uni_jsonp(self, session_info):
        request = self.make_request(session_info)
        try:
            with cedexis.radar.session.closing_urlopen(request, timeout=10) as f:
                response_text = f.read().decode().strip()
            logger.debug('UNI JSONP response text: %s', response_text)

            end_slice = -2
            if not response_text.endswith(';'):
                end_slice = -1
            response_text = response_text[8:end_slice]
            logger.debug('Slice: %s', response_text)
            data = json.loads(response_text.replace("'", '"'))
            logger.debug('UNI JSON data: %s', pformat(data))
            self.__provider['uni'] = data['node']
        except url_error as e:
            self.__provider['uni'] = '0'

def measure_provider(session_info, data):
    """Measure a provider's probes.  Return a list containing the report data"""
    provider_data = {
        'r_zid': data['r']['z'],
        'r_cid': data['r']['c'],
        'p_o_zid': data['p']['z'],
        'p_o_cid': data['p']['c'],
        'pid': data['p']['i'],
        'cache_busting': data['p']['b'],
        'continue': True,
        'uni': '0',
    }
    logger.debug('Measuring provider: %s', provider_data['pid'])
    result = []
    for probe in [ Probe(provider_data, probe_spec) for probe_spec in data['p']['p'] ]:
        if not provider_data['continue']:
            break
        try:
            if probe.is_uni_ajax:
                probe.get_uni_ajax(session_info)
            elif probe.is_uni_jsonp:
                probe.get_uni_jsonp(session_info)
            else:
                result.append(probe.measure(session_info))
        except cedexis.radar.session.errors.InvalidThroughputFileSizeError:
            break
        except cedexis.radar.session.errors.UnexpectedHttpStatusError as e:
            logger.warning(
                'Unexpected HTTP status when measuring provider id %s: %s %s',
                provider_data['pid'],
                e.status,
                e.text
            )
            break

    return result
