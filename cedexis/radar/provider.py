import logging
from pprint import pformat
import collections

logger = logging.getLogger(__name__)

import cedexis.radar.probe

class Provider(object):

    def __init__(self, config, requestor_zid, requestor_cid, transaction_id,
        request_signature, tracer, secure, report_server):
        super(Provider, self).__init__()

        def make_probe(probe_id):
            return cedexis.radar.probe.Probe(
                probe_data['u'],
                probe_data['t'],
                probe_id,
                requestor_zid,
                requestor_cid,
                provider_data['z'],
                provider_data['c'],
                provider_data['i'],
                transaction_id,
                request_signature,
                tracer,
                secure,
                report_server
            )

        provider_data = {}
        if 'p' in config:
            provider_data = config['p']

        self.__probes = collections.deque()
        if 'p' in provider_data:
            probes_data = provider_data['p']
            for protocol_key in [ 'a', 'b' ]:
                if protocol_key in probes_data:
                    protocol_probes = probes_data[protocol_key]
                    if 'a' in protocol_probes:
                        probe_data = protocol_probes['a']
                        self.__probes.append(make_probe(1))
                    if 'b' in protocol_probes:
                        probe_data = protocol_probes['b']
                        self.__probes.append(make_probe(0))
                    if 'c' in protocol_probes:
                        probe_data = protocol_probes['c']
                        self.__probes.append(make_probe(14))


    def measure(self):
        logger.debug('Inside Provider.measure')
        while 0 < len(self.__probes):
            self.__probes.popleft().measure()
