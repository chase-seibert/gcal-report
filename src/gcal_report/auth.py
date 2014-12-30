import tempfile

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from oauth2client.file import Storage


def generate_access_token(client_id, client_secret):
    flow = OAuth2WebServerFlow(
        client_id=client_id,
        client_secret=client_secret,
        scope='https://www.googleapis.com/auth/calendar.readonly',
        redirect_uri='http://example.com/auth_return')
    tmp = tempfile.NamedTemporaryFile()
    storage = Storage(tmp.name)
    credentials = run(flow, storage)
    return credentials.access_token
