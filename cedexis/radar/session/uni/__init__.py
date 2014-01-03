
import re

from cedexis.radar.session.uni.unireader import UniReader, BrokenUniReader
from cedexis.radar.session.uni.cloudfront import Cloudfront
from cedexis.radar.session.uni.akamai_r import Akamai_R
from cedexis.radar.session.uni.limelight import Limelight
from cedexis.radar.session.uni.chinacache import ChinaCache

providers = {
    14: Cloudfront(),
    17: ChinaCache(),
    18: UniReader(re.compile('x-hw:\s+(.+)', re.IGNORECASE), replacement=(',', '@')),
    19: UniReader(re.compile('x-cache:\s+[A-Z]{3,4}\s+from\s+\w+\-\w+\-\w+\.([a-z0-9]+)\.internap\.com', re.IGNORECASE)),
    20: Limelight(),
    24: UniReader(re.compile('server: ecs \(([\w]+)\/[\w]+\)', re.IGNORECASE)),
    32: UniReader(re.compile('x-wr-diag:\s+host:(\d+)', re.IGNORECASE), request_headers={ 'x-wr-diag': 'host' }),
    35: UniReader(re.compile('via:\s+[0-9]\.[0-9]\s+\w+\.(\w+)\.', re.IGNORECASE)),
    78: UniReader(re.compile('x-hw:\s+(.+)', re.IGNORECASE)),
    112: UniReader(re.compile('server: ecs \(([\w]+)\/[\w]+\)', re.IGNORECASE)),
    #275: UniReader(re.compile('x-server:\s\w+\.(\w+)\.netdna.com', re.IGNORECASE)),
    275: BrokenUniReader(),
    276: UniReader(re.compile('x-cf1:\s\w+\.(\w+):', re.IGNORECASE)),
    287: Akamai_R(),
}
