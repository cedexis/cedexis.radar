
import re
import logging

logger = logging.getLogger(__name__)

from cedexis.radar.session.uni.unireader import UniReader

class ChinaCache(UniReader):

    def __init__(self):
        super(ChinaCache, self).__init__()

    def try_get_uni(self, header):
        match = re.match('powered-by-chinacache:\s+[A-Z]+([A-Z])\s+from\s+([A-Z\-0-9]+)', header, re.IGNORECASE)
        if match:
            logger.debug('matche groups: %s', match.groups())
            return '{}_{}'.format(match.group(1), match.group(2))
