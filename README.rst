=============
cedexis.radar
=============

This package provides a library that can be used to conduct Cedexis Radar
measurements in any language that supports Python bindings.  It also
provides a script that can be used to run a Radar session from the command
line.

Command Line Tool
=================

Configuration File
------------------

The tool uses an optional configuration file to control things such as
logging.  You may specify the path to this file either by using the
--config-file/-f command line argument, or by setting the PYTHON_RADAR_CONFIG
environment variable.  The --config-file/-f argument always takes precedence
over the environment variable setting.

The configuration file is JSON-formatted.  An example is shown below::

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

If you don't pass the --config-file/-f argument and the PYTHON_RADAR_CONFIG
environment variable is not set, or if you pass the --config-file/-f argument
with no value, the script uses default settings.  The default settings produce
minimal logging to the screen and no file logging.
