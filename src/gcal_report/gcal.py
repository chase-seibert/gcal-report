import datetime
from dateutil.parser import parse

import httplib2
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from oauth2client.file import Storage

from gcal_report import auth
from gcal_report import settings


MAX_MINUTES_PER_EVENT = 1440  # one day


def _build_service():
    http = auth.get_authorized_http()
    return build('calendar', 'v3', http=http)


def get_calendar_list():
    service = _build_service()
    # TODO pagination
    calendars = service.calendarList().list().execute()
    ids = []
    for item in calendars.get('items'):
        ids.append(item.get('id'))
    return sorted(ids)


def _format_time(date):
    _datetime = datetime.datetime
    isoformat = _datetime.combine(date, _datetime.min.time()).isoformat()
    return isoformat + '.000Z'


def _parse_date(date_str):
    return parse(date_str)


def _minute_diff(start, end):
    return int((end - start).total_seconds() / 60)


def get_calendar_events(calendar_id, start, end, pageToken=None):

    service = _build_service()
    events = (service
        .events()
        .list(
            calendarId=calendar_id,
            timeMin=_format_time(start),
            timeMax=_format_time(end),
            pageToken=pageToken,
        )
        .execute())

    results, seen = [], []

    # pagination, see: https://developers.google.com/calendar/v3/pagination
    for event in events.get('items'):

        id = event['id']
        if id in seen:
            continue
        seen.append(id)

        status = event['status']
        if status in ('cancelled', ):
            continue

        _start = event['start']
        if 'dateTime' not in _start:
            # all-day events
            continue

        start_datetime = _parse_date(_start['dateTime'])
        end_datetime = _parse_date(event['end']['dateTime'])
        minutes = _minute_diff(start_datetime, end_datetime)

        if start_datetime.date() < start or end_datetime.date() > end:
            # api can return items updated between timeMin and timeMax
            continue

        if minutes > MAX_MINUTES_PER_EVENT:
            continue

        result = {
            'id': event['id'],
            'title': event.get('summary', None),
            'datetime': start_datetime,
            'date': start_datetime.date(),
            'minutes': minutes,
        }

        results.append(result)

    nextPageToken = events.get('nextPageToken')
    if nextPageToken:
        results.extend(get_calendar_events(calendar_id, start, end, nextPageToken))

    return sorted(results, key=lambda e: e['datetime'])
