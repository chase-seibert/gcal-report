import httplib2
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from oauth2client.file import Storage


from gcal_report import settings


# see: https://github.com/googleapis/google-api-python-client/blob/master/docs/README.md
def generate_access_token(client_id, client_secret):
    flow = OAuth2WebServerFlow(
        client_id=client_id,
        client_secret=client_secret,
        scope='https://www.googleapis.com/auth/calendar.readonly',
        # see https://stackoverflow.com/questions/8546907/google-calendar-api-v3-how-to-obtain-a-refresh-token-python
        access_type='offline',  # get a refresh token
        approval_prompt='force',  # needed for refresh token
        redirect_uri='http://example.com/auth_return')
    storage = Storage(settings.CREDS_FILE)
    credentials = run(flow, storage)
    return credentials.access_token


def get_authorized_http():
    storage = Storage(settings.CREDS_FILE)
    credentials = storage.get()
    http = httplib2.Http()
    if not credentials:
        print 'Invalid credentials, run `./run.sh login`'
        exit(1)
    if credentials.invalid:
        if credentials.access_token_expired and credentials.refresh_token:
            credentials.refresh(http)  # still needs to be authorized bellow
    return credentials.authorize(http)
