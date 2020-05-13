import os


CREDS_FILE = os.path.expanduser('~/.gcal-report-creds')
CACHE_FILE = os.path.expanduser('~/.gcal-report-cache.json')

DOMAIN = '@example.com'

TEAMS = {
    'name': [
        'user1',
        'user2',
    ],
}

try:
    from gcal_report.settings_override import *
except ImportError:
    pass
