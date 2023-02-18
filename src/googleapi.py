from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from config import Config
import os
import io

class googleapis:

    SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly', 
    'https://www.googleapis.com/auth/drive.readonly'
]
    
    SAMPLE_RANGE_NAME = 'Main!A2:L'
    SPREADSHEET_ID = Config.getkeys()['spreadsheetid']

    @staticmethod
    def creds():
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.abspath('config/token.json')):
            creds = Credentials.from_authorized_user_file(os.path.abspath('config/token.json'), googleapis.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.abspath('config/credentials.json'), googleapis.SCOPES)
                # flow = InstalledAppFlow.from_client_secrets_file(
                #     resource_path('../config/credentials.json'), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(os.path.abspath('config/token.json'), 'w') as token:
                token.write(creds.to_json())

            return creds

    @staticmethod
    def sheetsapi():        
        try:
            service = build('sheets', 'v4', credentials=googleapis.creds(), static_discovery=False)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=googleapis.SPREADSHEET_ID,
                                        range=googleapis.SAMPLE_RANGE_NAME).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
                return

            return values
        
        except HttpError as err:
            print(err)

    @staticmethod
    def driveapi(dlink,fmaindir):
        try:
            service = build('drive', 'v3', credentials=googleapis.creds(), static_discovery=False)

            # Call the Drive v3 API
            results = service.files().list(
                q = '"174Gu0skBr3sVf9pxwcXPg9R6FVlaOPBor_6-NuOWIcC8bcPYsVsQc-vSeszOrpkAQ-KftNTx" in parents and trashed = false', pageSize=1000, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            
            for item in items:
                if dlink[33:] == item['id']:
                    request = service.files().get_media(fileId=item['id'])

                    file = io.FileIO(fmaindir + "\\" + item['name'],'w')
                    downloader = MediaIoBaseDownload(file, request)
                    done = False
                    print(f'Downloading {item["name"]} 0%.')
                    while done is False:
                        status, done = downloader.next_chunk()
                        print(f'Downloading {item["name"]} {int(status.progress() * 100)}%.')         
                    return item['name']

        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')
