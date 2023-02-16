from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime
from pathlib import Path
import os
from funcs import *


# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly', 
    'https://www.googleapis.com/auth/drive.readonly'
]

# The ID and range of the spreadsheet.
SPREADSHEET_ID = '1SdZGuAU3WBXOrxiPzJaFSoSTatwcYFy6tkEvsbU6uAE'
SAMPLE_RANGE_NAME = 'Main!A2:L'

# date related stuff
today = datetime.datetime.strptime(datetime.datetime.now().strftime('%d-%m-%Y'),'%d-%m-%Y')
weekday = datetime.datetime.weekday(today)

# Main Working Directory
maindir = os.path.join(Path.home(), f'Desktop\\AutoMM\\{satcalc(today,weekday)}\\')

# got from https://stackoverflow.com/a/44352931
def resource_path(relative_path):
    import sys
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


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
                resource_path(os.path.join(os.pardir,'credentials\\credentials.json')), SCOPES)
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

    # ----- start of file creation -----

        os.makedirs(os.path.dirname(maindir), exist_ok=True)

        dic = {
            'Momentos de Louvor':['MDL',0],
            'Culto':['C',0],
            'Escola Sabatina':['ES',0],
            'Anúncios':['AN',0],
            'Programa da Tarde':['PDT',0],
            'Momento Especial':['ME',0,{
                'Durante a Escola Sabatina':0,
                'Após a Escola Sabatina':0,
                'Antes do Culto':0,
                'Durante o Culto':0,
                'Após o Culto':0
            }]
        }

        # Start the bat file
        batfile = open(maindir + 'Open Me.bat','w')
        batfile.write('@echo off\n')

        # Start the txt file
        txtfile = open(maindir + f'{satcalc(today,weekday)}.txt','w')
        txtfile.write(f'Programa {satcalc(today,weekday)}\n\n')

    #TODO Adicionar auto video carta missionaria at some point
        for row in reversed(values):
            if today <= datetime.datetime.strptime(row[0], '%d/%m/%Y'):
                if row[1] == 'Momento Especial':
                    if dic['Momento Especial'][1] == 0:
                        batfile.write(f'start https://www.google.com/search?q=ME\n')
                        txtfile.write(f'{row[1]}')
                        dic['Momento Especial'][1] += 1
                    for time in dic['Momento Especial'][2].keys():
                        if time == row[10]:
                            if dic['Momento Especial'][2][row[10]] == 0:
                                if row[11] != 'Não':
                                    batfile.write(f'\nstart {row[11]}\n')
                                txtfile.write(f'\n{row[10]}\n{number_get(row[11])}\n\n')
                                if row[4] != '':
                                    txtfile.write(f'{necfiles(row[4],maindir,creds)}\n\n')
                                else:
                                    txtfile.write('\n')
                                dic['Momento Especial'][2][row[10]] += 1
                            else:
                                pass
                else:
                    file_writing(batfile,txtfile,row,dic,maindir,creds)

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
input('Finished.')
