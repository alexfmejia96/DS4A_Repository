from __future__ import print_function
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import io
from PIL import Image

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
QUERY_FOLDERS = "mimeType ='application/vnd.google-apps.folder'"

def get_service():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)

            creds = flow.run_local_server(port=6969)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    return(service)

def dl_drive_file(s, file_id):
    req = s.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, req)
    
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Progress: %d%%." % int(status.progress() * 100))
    
    return(Image.open(file))

class Service:

    def __init__(self):
        self.service = get_service()

    def get_service(self):
        return(self.service)

    def get_folder_list(self):
        s = self.service
        resp = s.files().list(q=QUERY_FOLDERS,
            spaces='drive',
            fields='nextPageToken, files(id, name)').execute()

        #List of folder with their ids
        folder_list = resp['files']
        return(folder_list)

    def get_files_infolder(self, parent_id):
        s = self.service
        resp = s.files().list(q=f"'{parent_id}' in parents and trashed = false",
                spaces='drive',
                fields='nextPageToken, files(id, name)').execute()

        file_list = resp['files']
        return(file_list)

    def download_files(self, file_ids):
        s = self.service
        file_bucket = []
        for file_id in file_ids:
            print('\n', f'>Downloading: {file_id}')
            file_bucket.append(dl_drive_file(s, file_id))

        return (file_bucket)


if __name__ == '__main__':
    pass