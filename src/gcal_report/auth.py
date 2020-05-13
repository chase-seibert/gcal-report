import httplib2
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from oauth2client.file import Storage


from gcal_report import settings


def generate_access_token(client_id, client_secret):
    flow = OAuth2WebServerFlow(
        client_id=client_id,
        client_secret=client_secret,
        scope='https://www.googleapis.com/auth/calendar.readonly',
        redirect_uri='http://example.com/auth_return')
    storage = Storage(settings.CREDS_FILE)
    credentials = run(flow, storage)
    return credentials.access_token


def get_authorized_http():
    storage = Storage(settings.CREDS_FILE)
    credentials = storage.get()
    # TODO: this can auto-reauth if needed...
    if credentials is None or credentials.invalid:
        print 'Invalid credentials, run `./run.sh login`'
        exit(1)
    http = httplib2.Http()
    return credentials.authorize(http)
