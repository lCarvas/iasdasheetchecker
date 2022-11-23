from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime
from pathlib import Path
import os


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1SdZGuAU3WBXOrxiPzJaFSoSTatwcYFy6tkEvsbU6uAE'
SAMPLE_RANGE_NAME = 'Main!A2:L'

maindir = os.path.join(Path.home(), 'Desktop\\AutoMM\\')
today = datetime.datetime.now().strftime('%d/%m/%Y')
today = datetime.datetime.strptime(today,'%d/%m/%Y')



def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds, static_discovery=False)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
            return
        
        os.makedirs(os.path.dirname(maindir), exist_ok=True)

        # Index Variables
        nhi = 0
        ci = 0
        esi = 0
        mei = 0

        # Start the bat file
        batfile = open(maindir + 'Open Me.bat','w')
        batfile.write('@echo off\n')

        for row in reversed(values):
            if today <= datetime.datetime.strptime(row[0], '%d/%m/%Y'):
                #TODO Create a txt file with the info necessary, 
                if row[1] == 'Novo Hinário':
                    if nhi == 0:
                        batfile.write(f'::Novo Hinário\nstart {row[2]}\nstart {row[3]}\n\n')
                        nhi += 1
                    else:
                        pass

                elif row[1] == 'Culto':
                    if ci == 0:
                        batfile.write(f'::Culto\nstart {row[2]}\nstart {row[3]}\n\n')
                        ci += 1
                    else: 
                        pass
                
                #TODO Adicionar auto video carta missionaria at some point
                elif row[1] == 'Escola Sabatina':
                    if esi == 0:
                        batfile.write(f'::Escola Sabatina\nstart {row[2]}\nstart {row[3]}\n\n')
                        esi += 1
                    else:
                        pass
                
                elif row[1] == 'Momento Especial':
                    if mei == 0:
                        if row[11] == 'Não':
                            checkstart = '::Sem Música'
                        else:
                            checkstart = f'start {row[11]}'
                        batfile.write(f'::Momento Especial\n::{row[10]}\n{checkstart}\n\n')
                        mei += 1
                    else:
                        pass


    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()