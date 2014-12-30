from apiclient.discovery import build
import httplib2
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from oauth2client.file import Storage

from gcal_report import auth
from gcal_report import settings


def _build_service():
    http = auth.get_authorized_http()
    return build('calendar', 'v3', http=http)


def get_calendar_list():
    service = _build_service()
    calendars = service.calendarList().list().execute()
    ids = []
    for item in calendars.get('items'):
        ids.append(item.get('id'))
    return sorted(ids)
