try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'encrypted file transfer client and server',
    'author': 'Tyrone Lagore and James MacIsaac',
    'url': '',
    'download_url': 'https://github.com/jfizzy/cpsc_526_assignment3',
    'author_email': 'tyronelagore@gmail.com and james@jmproj.com',
    'version': '0.1',
    'install_requires': [],
    'packages': ['server', 'client'],
    'scripts': [],
    'name': 'ftp_secure'
}

setup(**config)
