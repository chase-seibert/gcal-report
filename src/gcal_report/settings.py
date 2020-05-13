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
