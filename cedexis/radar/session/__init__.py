
import sys
import os
import logging
import platform
from pprint import pformat
import contextlib

try:
    from urllib.request import urlopen
except ImportError:
    # Python 2
    from urllib2 import urlopen

logger = logging.getLogger(__name__)

import cedexis.radar

def make_ua_string(zone_id, customer_id, tracer):
    return 'PyRadar/{}.{}.{} ({} {}; {}) {}/{}{}'.format(
        cedexis.radar.__sampler_major_version__,
        cedexis.radar.__sampler_minor_version__,
        cedexis.radar.__sampler_micro_version__,
        platform.python_implementation(),
        platform.python_version(),
        platform.platform(),
        zone_id,
        customer_id,
        '' if tracer is None else '/{}'.format(tracer.strip())
    )

def closing_urlopen(request, timeout=None):
    kwargs = {} if timeout is None else { 'timeout': timeout }
    f = urlopen(request, **kwargs)
    if hasattr(f, '__exit__'):
        return f
    return contextlib.closing(f)
