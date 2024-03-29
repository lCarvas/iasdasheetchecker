from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os
import gdown
import sys

class googleapis:

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
    SAMPLE_RANGE_NAME = 'Main!A2:L'
    SPREADSHEET_ID = None

    @staticmethod
    def sheetsapi():  

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        try:
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
        except FileNotFoundError:
            print('Credentials file not found, have you put it in the config folder?')
            input('Press Enter to close the app.')
            sys.exit()


        try:
            service = build('sheets', 'v4', credentials=creds, static_discovery=False)

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
            print('Did you input the Spreadsheet id correctly?')

    @staticmethod
    def driveapi(dlink,fmaindir):
        gdown.download(url=dlink,fuzzy=True,use_cookies=False,output=(os.path.abspath(fmaindir) + '\\'))