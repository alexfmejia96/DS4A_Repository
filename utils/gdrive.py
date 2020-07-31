from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
from PIL import Image

SCOPES = ['https://www.googleapis.com/auth/drive']
QUERY_FOLDERS = "mimeType ='application/vnd.google-apps.folder'"

def dl_drive_file(s, file_id):
    req = s.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, req)
    
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Progress: %d%%." % int(status.progress() * 100))
    
    return(Image.open(file))

def get_raw_metadata(img):
    raw_metadata = img.getexif()
    return(raw_metadata)

class Service:

    def __init__(self):
        self.flow = Flow.from_client_secrets_file('../credentials.json',
            SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        self.auth_url, _ = self.flow.authorization_url(prompt='consent')
        self.service = None
        self.is_valid = None

    def auth_service(self, code):
        try:
            self.flow.fetch_token(code=code)
            self.credentials = self.flow.credentials
            self.service = build('drive', 'v3', credentials=self.credentials)
            self.is_valid = True
        except:
            self.is_valid = False
            print('>>Error in Service Auth')

    def get_service(self):
        return(self.service)

    def get_folder_list(self):
        s = self.service
        resp = s.files().list(q=QUERY_FOLDERS,
            spaces='drive',
            fields='nextPageToken, files(id, name)').execute()

        folder_list = resp['files']
        return(folder_list)

    def get_files_infolder(self, parent_id):
        s = self.service
        resp = s.files().list(q=f"'{parent_id}' in parents and trashed = false and mimeType = 'image/jpeg'",
                spaces='drive',
                fields='nextPageToken, files(id, name)').execute()

        file_list = resp['files']
        return(file_list)

    def download_files(self, img_items, dl_dir=None, in_ram=False):
        s = self.service
        image_list = []
        metadata_list = []

        for img_item in img_items:
            print(f">Downloading {img_item['name']}: {img_item['id']}")
            temp_file = dl_drive_file(s, img_item['id'])
            metadata_list.append(get_raw_metadata(temp_file))

            if in_ram:
                image_list.append(temp_file)
            else:
                temp_file_dir = '/'.join([dl_dir , img_item['name'].lower()])
                temp_file.save(temp_file_dir)
                image_list.append(temp_file_dir) 

            temp_file.close()

        
        return ([image_list, metadata_list])
