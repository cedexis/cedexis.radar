
import re

from cedexis.radar.session.uni.unireader import UniReader

class Cloudfront(UniReader):

    def __init__(self):
        super(Cloudfront, self).__init__(None)

    def uni_from_headers(self, headers):
        """Gotta check two headers"""
        first = None
        second = None
        for pair in headers:
            combined = ': '.join(pair)
            match_server = re.match('Via:\s\d\.\d\s(\w+)\.cloudfront.net', combined)
            match_rid = re.match('X-Amz-Cf-Id:\s+(.*)', combined)
            if match_server:
                first = match_server.group(1)
            if match_rid:
                second = match_rid.group(1)
        if first and second:
            return '{}@{}'.format(first, second)
        elif first:
            return first
        elif second:
            return second
        return '1'
