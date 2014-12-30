import httplib2
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from oauth2client.file import Storage

from gcal_report import settings


def get_calendar_list():
    creds = _get_access_token()
    print creds
