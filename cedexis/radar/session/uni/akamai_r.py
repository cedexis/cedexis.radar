
import re

from cedexis.radar.session.uni.unireader import UniReader

class Akamai_R(UniReader):

    def __init__(self):
        headers = { 'Pragma': 'akamai-x-cache-on' }
        super(Akamai_R, self).__init__(request_headers=headers)

    def try_get_uni(self, header):
        match = re.match('x-cache:\s+\w+\s+from\s+\w(\d+-\d+-\d+-\d+).*$', header, re.IGNORECASE)
        if match:
            return match.groups()[0].replace('-', '.')
