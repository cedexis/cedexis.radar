

class InvalidThroughputFileSizeError(Exception):
    pass

class UniNotFoundError(Exception):
    pass

class UnexpectedStatusError(Exception):
    pass

class UnexpectedHttpStatusError(Exception):
    def __init__(self, status, text):
        self.__status = status
        self.__text = text

    @property
    def status(self):
        return self.__status

    @property
    def text(self):
        return self.__text
