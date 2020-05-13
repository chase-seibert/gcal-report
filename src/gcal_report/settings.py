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

def event_is_meeting(event):
    # return False if you want to exclude a specific meeting
    # event is a dict with fields like summary, description, etc
    return False

try:
    from gcal_report.settings_override import *
except ImportError:
    pass
