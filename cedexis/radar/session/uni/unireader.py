
import cedexis.radar.session.errors

class UniReader(object):

    def __init__(self, regex=None, match_group=0, request_headers=None, replacement=None):
        self.__regex = regex
        self.__match_group = match_group
        self.__request_headers = request_headers
        self.__replacement = replacement

    @property
    def request_headers(self):
        return self.__request_headers

    def try_get_uni(self, header):
        """Default header test"""
        matches = self.__regex.match(header)
        if not matches is None:
            if not self.__replacement is None:
                return matches.groups()[self.__match_group].replace(*self.__replacement)
            return matches.groups()[self.__match_group]
        return None

    def uni_from_headers(self, headers):
        for pair in headers:
            uni = self.try_get_uni(': '.join(pair))
            if not uni is None:
                return uni
        raise session.errors.UniNotFoundError()

class BrokenUniReader(UniReader):

    def __init__(self):
        super(BrokenUniReader, self).__init__(None)

    def uni_from_headers(self, headers):
        return '0'
