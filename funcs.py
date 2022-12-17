from __future__ import print_function
import io
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# got from https://stackoverflow.com/a/44352931
def resource_path(relative_path):
    import sys
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def satcalc(ftoday,fweekday):
    import datetime
    if fweekday == 6:
        saturday = datetime.datetime.strftime(ftoday + datetime.timedelta(days=12-datetime.datetime.weekday(ftoday)), '%d-%m-%Y')  
    else:
        saturday = datetime.datetime.strftime(ftoday + datetime.timedelta(days=5-datetime.datetime.weekday(ftoday)), '%d-%m-%Y')
    
    return saturday

# got from https://stackoverflow.com/a/52664178
def number_get(Iurl):
    import urllib.request
    import json
    import urllib
    import validators
    from cleantext import clean

    params = {"format": "json", "url": "%s" % Iurl}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    if validators.url(Iurl):
        with urllib.request.urlopen(url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
            title = clean(data['title'], no_emoji=True)
    else:
        title = Iurl
    
    # got from https://stackoverflow.com/a/4510805
    for i, c in enumerate(title):
        if c.isdigit():
            title = title[i:i+3]
            break

    return title

def file_writing(batfile,txtfile,frows,fdic,fmaindir,fcreds):
    if fdic[f'{frows[1]}'][1] == 0:
        batfile.write(f'start https://www.google.com/search?q={fdic[f"{frows[1]}"][0]}\n')
        # Link hinos
        for i in range(2,4):
            if not frows[i].isdigit():
                batfile.write(f'start {frows[i]}\n')
        # Numero hinos
        txtfile.write(f'{frows[1]}\n{number_get(frows[2])}\n{number_get(frows[3])}\n\n')

        if frows[1] == 'Culto' or frows[1] == 'Escola Sabatina':
            # Programa Escola Sabatina
            if frows[1] == 'Escola Sabatina':
                txtfile.write(f'{frows[5]}\n\n')            
            # Doxologia
            elif frows[1] == 'Culto':
                batfile.write(f'start https://www.youtube.com/playlist?list=PL3sgRPOFYAyxahQy75UOv_wGlAvegskT_\n')
                for j in range(7,10):
                    if frows[j] != 'Normal':
                        batfile.write(f'start {frows[j]}\n')
                        txtfile.write(f'{number_get(frows[j])}\n\n')
                    else:
                        txtfile.write(f'{frows[j]}\n')
            # Ficheiros Necessários
            if frows[4] != '':
                txtfile.write(f'{necfiles(frows[4],fmaindir,fcreds)}\n\n')
            else:
                txtfile.write('\n')
        fdic[f'{frows[1]}'][1] += 1


def necfiles(dlink,fmaindir,fcreds):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    try:
        service = build('drive', 'v3', credentials=fcreds, static_discovery=False)

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
