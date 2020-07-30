from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']
QUERY_FOLDERS = "mimeType ='application/vnd.google-apps.folder'"

flow = Flow.from_client_secrets_file(
    'credentials2.json', SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
	
	#'urn:ietf:wg:oauth:2.0:oob' 'http://localhost:6969/'

# Tell the user to go to the authorization URL.
auth_url, state = flow.authorization_url(prompt='consent')
print(f'state: {state}')
print('Please go to this URL: {}'.format(auth_url))

# The user will get an authorization code. This code is used to get the
# access token.
code = input('Enter the authorization code: ')
flow.fetch_token(code=code)


s = build('drive', 'v3', credentials=flow.credentials)

resp = s.files().list(q=QUERY_FOLDERS,
    spaces='drive',
    fields='nextPageToken, files(id, name)').execute()
	
print(resp)