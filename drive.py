from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
DSCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def necfiles(dlink):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('tokendrive.json'):
        creds = Credentials.from_authorized_user_file('tokendrive.json', DSCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', DSCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('tokendrive.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            q = '"174Gu0skBr3sVf9pxwcXPg9R6FVlaOPBor_6-NuOWIcC8bcPYsVsQc-vSeszOrpkAQ-KftNTx" in parents and trashed = false', pageSize=1000, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        for item in items:
            if dlink[33:] == item['id']:
                return item['name']

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


