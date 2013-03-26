try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'BroadView API Client',
    'author': 'SensePost Pty Ltd',
    'url': 'http://www.sensepost.com',
    'download_url': '',
    'author_email': 'support@sensepost.com',
    'version': '0.1',
    'install_requires': [
        'nose',
        'python-dateutil',
        'nosy',
        'yanc',
        'requests'
    ],
    'packages': ['bvapi'],
    'scripts': [],
    'name': 'bvapi'
}

setup(**config)
