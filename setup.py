
from setuptools import setup, find_packages
import os
import re

def read_version():
    source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cedexis/radar/__init__.py')
    with open(source_path) as fp:
        source = fp.read()
    major_match = re.search('__sampler_major_version__\s*=\s*(\d+)', source)
    minor_match = re.search('__sampler_minor_version__\s*=\s*(\d+)', source)
    micro_match = re.search('__sampler_micro_version__\s*=\s*(\d+)', source)
    suffix_match = re.search('__version_suffix__\s*=\s*[\'"]([-\w\d]+)[\'"]', source)
    suffix = ''
    if not suffix_match is None:
        suffix = suffix_match.group(1)

    return '{}.{}.{}{}'.format(
        major_match.group(1),
        minor_match.group(1),
        micro_match.group(1),
        suffix,
    )

def read_file(file_path):
    """
    Read a file relative to the directory containing this file
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(root_dir, file_path)
    with open(file_path) as fp:
        content = fp.read()
        try:
            return content.decode('utf-8').strip()
        except AttributeError:
            return content.strip()

# See http://docs.python.org/3.3/distutils/apiref.html#module-distutils.core
# for help with setup keyword arguments
setup_kwargs = {
    # http://www.python.org/dev/peps/pep-0423/#use-a-single-name
    'name': 'cedexis.radar',
    'version': read_version(),
    'description': 'Cedexis Radar client library',
    'long_description': '\n\n'.join([
        read_file('README.rst'),
        read_file('CHANGES.rst'),
    ]),
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: IronPython',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    'keywords': [
        'cedexis',
        'radar',
        'internet',
        'dns',
        'cdn',
        'cloud',
        'load balancing',
        'availability',
        'rtt',
        'mobile',
    ],
    'url': 'https://github.com/cedexis/python-radar',
    'author': 'Jacob Wan',
    'author_email': 'jacob@wildlemur.com',
    'license': 'MIT',
    'packages': find_packages(),
    'namespace_packages': [
        'cedexis',
    ],
    'tests_require': [
        'nose'
    ],
    'test_suite': 'nose.collector',
    'entry_points': {
        'console_scripts': [
            'cedexis-radar-cli=cedexis.radar.cli:main',
        ],
    },
    'zip_safe': True,
}

setup(**setup_kwargs)
