
import datetime
import logging
import os

class TimestampedFileHandler(logging.FileHandler):

    def __init__(self, filename_template):
        filename = datetime.datetime.utcnow().strftime(filename_template)
        containing_dir = os.path.dirname(filename)
        if not os.path.isdir(containing_dir):
            os.makedirs(containing_dir)
        super(TimestampedFileHandler, self).__init__(filename)
