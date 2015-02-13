Changes
=======

0.1.7
-----

- Another error handling bug.

0.1.6
-----

- Fix error handling bug.

0.1.5
-----

- Init response handling.

0.1.4-1
-------

- cedexis.radar._crlogging.TimestampedFileHandler accepts the template for a
  complete path (not just the filename).  This provides greater control over
  the directory structure and filenames produced.

0.1.4
-----

- Provide cedexis.radar._crlogging.TimestampedFileHandler class.  This class
  allows you to isolate session log data in separate files.

0.1.3
-----

- Log warnings if any timeouts or exceptions occur.

0.1.2
-----

**cedexis-radar-cli**

- Support setting zone id and customer id in the configuration file.

0.1.1-2
-------

- Minor refactoring

- Support running cedexis-radar-cli directly

0.1.1-1
-------

**project**

- CHANGES.rst markup must be consistent with README.rst

0.1.1
-----

**project**

- Update README.rst

**cedexis-radar-cli**

- CEDEXIS_RADAR_CONFIG environment variable instead of PYTHON_RADAR_CONFIG

0.1.0-3
-------

**setup**

- CHANGES.rst was not being included in PKG-INFO when built under Python 3.

0.1.0-2
-------

**project**

- Update README.rst.

0.1.0-1
-------

**project**

- Add CHANGES.rst.

**setup**

- Fix a Python 3 bug in setup.py.

**cedexis-radar-cli**

- User can specify the default options by passing the --config-file/-f
  argument with no value.

0.1.0
-----

Initial implementation.
