import argparse
import ConfigParser
import datetime
import os
import pprint
import sys

from gcal_report import auth
from gcal_report import cache
from gcal_report import gcal
from gcal_report import settings
from gcal_report.report import GCalReport


def login(options):
    client_id = settings.CLIENT_ID or raw_input('Client ID: ')
    client_secret = settings.CLIENT_SECRET or raw_input('Client secret: ')
    access_token = auth.generate_access_token(client_id, client_secret)
    print 'Success'


def print_list(options):
    for calendar_id in gcal.get_calendar_list():
        print calendar_id


def _get_calendar_ids(team):
    try:
        ids = settings.TEAMS[team]
        domain = settings.DOMAIN
        if domain:
            ids = [(id + domain if '@' not in id else id) for id in ids]
        return ids
    except KeyError:
        print 'Team %s not defined' % team
        exit(1)


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

    _auth = subparsers.add_parser('login')
    _auth.set_defaults(func=login)

    _list = subparsers.add_parser('list')
    _list.set_defaults(func=print_list)

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
    cache.load()
    parser = create_arg_parser()
    options = parser.parse_args(sys.argv[1:])
    options.func(options)
    cache.update()

if __name__ == '__main__':
    main()
