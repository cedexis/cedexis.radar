
try:
    from urllib.parse import urlencode, urlunparse, urlparse, parse_qsl
    from urllib.request import Request, urlopen
    from urllib.error import URLError as url_error
except ImportError:
    # Python 2
    from urlparse import urlunparse, urlparse, parse_qsl
    from urllib import urlencode
    from urllib2 import Request, URLError as url_error, urlopen

import random
import string
import logging
from pprint import pprint
import time

logger = logging.getLogger(__name__)

import cedexis.radar.session

class Probe(object):

    def __init__(self, url, typecode, probe_id, requestor_zid, requestor_cid,
        provider_zid, provider_cid, pid, transaction_id, request_signature,
        tracer, secure, report_server):
        super(Probe, self).__init__()
        self.__url = url
        self.__typecode = typecode
        self.__probe_id = probe_id
        self.__requestor_zid = requestor_zid
        self.__requestor_cid = requestor_cid
        self.__provider_zid = provider_zid
        self.__provider_cid = provider_cid
        self.__pid = pid
        self.__transaction_id = transaction_id
        self.__request_signature = request_signature
        self.__tracer = tracer
        self.__secure = secure
        self.__report_server = report_server

    def __repr__(self):
        return 'cedexis.radar.probe.Probe; {}, {}'.format(self.__url, self.__typecode)

    def measure(self):

        def get_elapsed():
            stop = stopwatch()
            logger.debug('Start: %s; Stop: %s', start, stop)
            elapsed = stop - start
            #logger.debug('Elapsed: %s seconds', elapsed)
            elapsed *= 1000
            elapsed = int(round(elapsed))
            logger.debug('Elapsed: %s milliseconds', elapsed)
            return elapsed

        def get_filesize():
            return 100

        def calculate_throughput():
            result = 8 * 1000 * get_filesize() // elapsed
            return result

        logger.debug('Inside Probe.measure; {}'.format(self))
        query_string = self.make_query_string()
        parts = urlparse(self.__url)
        parts = (
            parts.scheme,
            parts.netloc,
            parts.path,
            parts.params,
            query_string,
            parts.fragment
        )
        url = urlunparse(parts)
        logger.debug('Probe URL: {}'.format(url))
        request = Request(url)

        try:
            stopwatch = time.perf_counter
        except AttributeError:
            # Python <3.3
            stopwatch = time.time

        start = stopwatch()
        f = None
        ok = True
        result_code = 0
        try:
            f = urlopen(request)
            content = f.read()
        except url_error as e:
            ok = False
            result_code = 4
            print(e, url)
        finally:
            if not f is None:
                f.close()

        measurement = 0
        if ok:
            elapsed = get_elapsed()
            if 4000 >= elapsed:
                measurement = elapsed
                if 14 == self.__probe_id:
                    measurement = calculate_throughput()
            else:
                result_code = 1
        logger.debug('Result code: {}, Measurement: {}'.format(result_code, measurement))
        self.send_report(result_code, measurement)

    def send_report(self, result_code, measurement):
        path_parts = [
            'f1',
            self.__request_signature,
            str(self.__provider_zid),
            str(self.__provider_cid),
            str(self.__pid),
            str(self.__probe_id),
        ]
        path_parts.append(str(result_code))
        path_parts.append(str(measurement))
        path_parts.append('1')
        path_parts.append('1')

        query_string = urlencode({
            'rnd': ''.join(random.choice(string.ascii_letters + string.digits) for i in range(30))
        })

        parts = (
            'https' if self.__secure else 'http',
            'rpt.cedexis.com' if self.__report_server is None else self.__report_server,
            '/'.join(path_parts),
            '',
            query_string,
            ''
        )
        url = urlunparse(parts)
        logger.debug('Report URL: {}'.format(url))

        user_agent_string = cedexis.radar.session.make_ua_string(
            self.__requestor_zid,
            self.__requestor_cid,
            self.__tracer,
        )
        headers = {
            'User-Agent': user_agent_string
        }
        request = Request(url, headers=headers)
        try:
            f = urlopen(request)
            content = f.read()
            # print(content)
        except url_error as e:
            print(e, url)
        finally:
            if not f is None:
                f.close()

    def make_query_string(self):
        qs_data = '-'.join([
            str(self.__probe_id),
            str(self.__requestor_zid),
            str(self.__requestor_cid),
            str(self.__provider_zid),
            str(self.__provider_cid),
            str(self.__pid),
            str(self.__transaction_id),
            self.__request_signature
        ])
        # print(qs_data)
        return qs_data

    def get_cache_buster(self):
        if self.__cache_busting:
            return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(30))
        return None
