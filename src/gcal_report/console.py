import argparse
import ConfigParser
import datetime
import os
import pprint
import sys

from gcal_report import auth
from gcal_report import gcal
from gcal_report import settings
from gcal_report.report import GCalReport


def init(options):
    print 'Create a new project: https://console.developers.google.com/project'
    print 'IMPORTANT: Set Redirect URI to http://localhost:8080'
    client_id = raw_input('Client ID: ')
    client_secret = raw_input('Client secret: ')
    settings.update_section('Credentials', {
        'client_id': client_id,
        'client_secret': client_secret,
    })


def login(options):
    client_id = settings.get_setting('Credentials', 'client_id')
    client_secret = settings.get_setting('Credentials', 'client_secret')
    access_token = auth.generate_access_token(client_id, client_secret)
    settings.update_section('Authentication', {
        'access_token': access_token,
    })


def print_list(options):
    for calendar_id in gcal.get_calendar_list():
        print calendar_id


def add(options):
    team_name = options.team
    team_calendar_ids = settings.get_setting('Teams', team_name, '').split(',')
    team_calendar_ids.append(options.id)
    team_calendar_ids = list(id for id in set(team_calendar_ids) if id)
    team_calendar_ids = ','.join(team_calendar_ids)
    settings.update_section('Teams', {
        team_name: team_calendar_ids,
    })


def _get_calendar_ids(team):
    try:
        ids = settings.get_setting('Teams', team).split(',')
        domain = settings.get_setting('Settings', 'domain')
        if domain:
            ids = [(id + domain if '@' not in id else id) for id in ids]
        return ids
    except KeyError:
        print 'Team %s not defined' % team


def _get_relative_date_range(days_ago):
    today = datetime.date.today()
    start = today - datetime.timedelta(days=days_ago)
    return start, today


def gen_gcal_report(options):
    calendar_ids = _get_calendar_ids(options.team)
    start, end = _get_relative_date_range(options.days)
    report = GCalReport(start, end)
    for calendar_id in calendar_ids:
        events = gcal.get_calendar_events(calendar_id, start, end)
        report.add_events(calendar_id, events)
    return report


def dump(options):
    report = gen_gcal_report(options)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(report.dump())


def report(options):
    report = gen_gcal_report(options)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(report.summary())


def csv(options):
    report = gen_gcal_report(options)
    report.csv(options.output)


def top(options):
    report = gen_gcal_report(options)
    for title, minutes in report.get_top_meetings(options.limit):
        print '%s (%s)' % (title, minutes)


def create_arg_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    _init = subparsers.add_parser('init')
    _init.set_defaults(func=init)

    _auth = subparsers.add_parser('login')
    _auth.set_defaults(func=login)

    _list = subparsers.add_parser('list')
    _list.set_defaults(func=print_list)

    _add = subparsers.add_parser('add')
    _add.set_defaults(func=add)
    _add.add_argument('--team', help='Team name', required=True)
    _add.add_argument('--id', help='Calendar ID', required=True)

    _dump = subparsers.add_parser('dump')
    _dump.set_defaults(func=dump)
    _dump.add_argument('--team', help='Team name', required=True)
    _dump.add_argument('--days', help='Days', type=int, default=90)

    _report = subparsers.add_parser('report')
    _report.set_defaults(func=report)
    _report.add_argument('--team', help='Team name', required=True)
    _report.add_argument('--days', help='Days', type=int, default=90)

    _csv = subparsers.add_parser('csv')
    _csv.set_defaults(func=csv)
    _csv.add_argument('--team', help='Team name', required=True)
    _csv.add_argument('--output', help='Output CSV file path', type=str, required=True)
    _csv.add_argument('--days', help='Days', type=int, default=90)

    _top = subparsers.add_parser('top')
    _top.set_defaults(func=top)
    _top.add_argument('--team', help='Team name', required=True)
    _top.add_argument('--days', help='Days', type=int, default=90)
    _top.add_argument('--limit', help='Limit', type=int, default=10)

    return parser


def main():
    parser = create_arg_parser()
    options = parser.parse_args(sys.argv[1:])
    options.func(options)


if __name__ == '__main__':
    main()
