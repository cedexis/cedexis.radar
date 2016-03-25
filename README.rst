=============
cedexis.radar
=============

This package provides a library that can be used to conduct Cedexis Radar
measurements in any language that supports Python bindings.  It also
provides a script that can be used to run a Radar session from the command
line.

To make practical use of its features, you should sign up for a free Cedexis_
account.  Your Cedexis customer id is a required argument to the main API
call and the command line tool.

Requires: **Python 2.7+**

Installation
============

Using pip
---------

The preferred method on platforms that support it is to install the package
using pip::

    $ pip install cedexis.radar

.. tip::

   On some platforms, you make need to preface this command with :code:`sudo -H`

From source
-----------

You can also install the package from source::

    $ cd /tmp
    $ git clone https://github.com/cedexis/cedexis.radar
    $ cd cedexis.radar
    $ python setup.py install

Command Line Tool
=================

Installation includes a command line tool called cedexis-radar-cli, which is
a shim for the "main" function in the cedexis.radar.cli module.

Usage
-----

Example::

    $ cedexis-radar-cli -c 10660
    2.7.5+ (default, Sep 19 2013, 13:48:49)
    [GCC 4.8.1]
    cedexis.radar.cli (INFO): Config file used:
    cedexis.radar.cli (INFO): Command line args: Namespace(api_key='sandbox', config_file='', customer_id=10660, provider_id=None, secure=False, tracer=None, zone_id=1)
    cedexis.radar (INFO): 2 providers measured

Full argument list:

+------------------+-----------------------------------------+
| Argument         | Description                             |
+==================+=========================================+
| --help/-h        | **HELP**                                |
|                  |                                         |
|                  | Show a help message and exit            |
+------------------+-----------------------------------------+
| --zone-id/-z     | **ZONE_ID**                             |
|                  |                                         |
|                  | Your Cedexis Zone ID (defaults to 1)    |
+------------------+-----------------------------------------+
| --customer-id/-c | **CUSTOMER_ID**                         |
|                  |                                         |
|                  | Your Cedexis Customer ID                |
+------------------+-----------------------------------------+
| --api-key/-k     | **API_KEY**                             |
|                  |                                         |
|                  | Reserved for future use                 |
+------------------+-----------------------------------------+
| --secure/-s      | **Use HTTPS**                           |
|                  |                                         |
|                  | If specified, only measure providers    |
|                  | configured with HTTPS probes            |
+------------------+-----------------------------------------+
| --tracer/-t      | **TRACER**                              |
|                  |                                         |
|                  | An optional value to be included in the |
|                  | user agent string. Useful for           |
|                  | troubleshooting.                        |
+------------------+-----------------------------------------+
| --provider-id/-p | **PROVIDER_ID**                         |
|                  |                                         |
|                  | Measure a specific provider and quit    |
+------------------+-----------------------------------------+
| --config-file/-f | **CONFIG_FILE**                         |
|                  |                                         |
|                  | Path to a configuration file            |
+------------------+-----------------------------------------+

Configuration File
------------------

The tool uses an optional configuration file to setup logging.  You may specify
the path to this file either using the --config-file/-f command line argument,
or by setting the CEDEXIS_RADAR_CONFIG environment variable.
The --config-file/-f argument always takes precedence over the environment
variable setting.

The configuration file is JSON-formatted.  The example below shows how to
setup verbose output to a file and reduced output to the console.

::

    {
        "customer": {
            "zone_id": 1,
            "customer_id": 10660
        },
        "logging": {
            "version": 1,
            "disable_existing_loggers": false,
            "formatters": {
                "console_formatter": {
                    "format": "%(name)s (%(levelname)s): %(message)s"
                },
                "file_formatter": {
                    "format": "%(asctime)s - %(name)s (%(levelname)s): %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "console_formatter"
                },
                "file": {
                    "class": "logging.FileHandler",
                    "level": "DEBUG",
                    "formatter": "file_formatter",
                    "filename": "/home/freddy/logs/cedexis.radar.log"
                }
            },
            "root": {
                "level": "DEBUG",
                    "handlers": [ "console", "file" ]
            }
        }
    }

If you don't pass the --config-file/-f argument and the CEDEXIS_RADAR_CONFIG
environment variable is not set, or if you pass the --config-file/-f argument
with no value, the script uses default settings.  The default settings produce
minimal logging to the screen and no file logging.

Unit Tests
==========

It's easy to run the unit test suite using `nose`_.  Here's an example for
Python 3 on Ubuntu 13.10.  It should be simple to adapt this example to other
operating systems and versions of Python.

::

    # Make sure you've got nose installed
    $ pip3 install nose

    # Run tests
    $ nosetests --with-xunit

.. _Cedexis:

About Cedexis
=============

Founded in 2009, Cedexis optimizes web performance across data centers, content
delivery networks (CDNs) and clouds, for companies that want to ensure 100%
availability and extend their reach to new global markets.

We provide real-time, data-driven, global traffic management solutions.
Optimize clouds, data centers and CDN content delivery to improve the
availability, latency and throughput of your website and other
Internet-connected apps, for every user on the globe.

Please visit us at `www.cedexis.com`_.

.. _`www.cedexis.com`: http://www.cedexis.com
.. _`nose`: https://nose.readthedocs.org/en/latest/
