=======
pyradar
=======

Run a standard Radar session anywhere with Python and an Internet connection.

Config File
===========

You can specify an optional config file to control things such as logging.

Example::

    {
        "logging": {
            "version": 1,
            "disable_existing_loggers": false,
            "formatters": {
                "console_formatter": {
                    "format": "%(name)s (%(levelname)s): %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "console_formatter"
                }
            },
            "root": {
                "level": "DEBUG",
                    "handlers": [ "console" ]
            }
        }
    }
