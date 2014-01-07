
import datetime
import logging

class TimestampedFileHandler(logging.FileHandler):

    def __init__(self, filename_template):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')
        filename = filename_template.format(now)
        super(TimestampedFileHandler, self).__init__(filename)
