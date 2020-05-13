from dateutil.parser import parse

from gcal_report import settings


MAX_MINUTES_PER_EVENT = 240  # arbitrary filter for fake calendar items


def _parse_date(date_str):
    return parse(date_str)


def _minute_diff(start, end):
    return int((end - start).total_seconds() / 60)


def count_as_meeting_time(event, user):

    status = event.get('status')
    description = event.get('description')
    kind = event.get('kind')
    summary = event.get('summary')
    location = event.get('location')
    attendees = event.get('attendees', [])
    num_attendees = len(attendees)
    start = event.get('start', {}).get('dateTime')
    end = event.get('end', {}).get('dateTime')
    creator = event.get('creator', {}).get('email')

    if status in ('cancelled', ):
        return False

    if not start:
        # all day events
        return False

    start_datetime = _parse_date(start)
    end_datetime = _parse_date(end)
    minutes = _minute_diff(start_datetime, end_datetime)

    if minutes > MAX_MINUTES_PER_EVENT:
        return False

    if creator == user and num_attendees == 0:
        # personal placeholder
        return False

    if hasattr(settings, 'event_is_meeting'):
        result = settings.event_is_meeting(event)
        if result is None:
            return True
        return result

    # print user, creator, repr(summary), num_attendees, start
    # import ipdb; ipdb.set_trace()
    return True
