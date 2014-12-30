import argparse
import ConfigParser
import os
import sys

from gcal_report import auth
from gcal_report import gcal
from gcal_report import settings


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


def list(options):
    print gcal.get_calendar_list()


def create_arg_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    _init = subparsers.add_parser('init')
    _init.set_defaults(func=init)

    _auth = subparsers.add_parser('login')
    _auth.set_defaults(func=login)

    _list = subparsers.add_parser('list')
    _list.set_defaults(func=list)

    return parser


def main():
    parser = create_arg_parser()
    options = parser.parse_args(sys.argv[1:])
    options.func(options)


if __name__ == '__main__':
    main()
