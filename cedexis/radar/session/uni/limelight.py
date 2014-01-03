
import re

from cedexis.radar.session.uni.unireader import UniReader

class Limelight(UniReader):

    def __init__(self):
        super(Limelight, self).__init__(request_headers={ 'x-ldebug': '1' })

    def try_get_uni(self, header):
        match = re.match('x-cache:\s\w+\sfrom\s[\.a-z]+\d+\.(\w+)\.llnw.net', header, re.IGNORECASE)
        if match:
            return match.groups()[0].replace('-', '.')
