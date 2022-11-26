def satcalc(ftoday,fweekday):
    import datetime
    if fweekday == 6:
        saturday = ftoday + datetime.timedelta(days=12-datetime.datetime.weekday(ftoday))  
    else:
        saturday = datetime.datetime.strftime(ftoday + datetime.timedelta(days=5-datetime.datetime.weekday(ftoday)), '%d-%m-%Y')
    
    return saturday

# got from https://stackoverflow.com/a/52664178
def number_get(Iurl):
    import urllib.request
    import json
    import urllib
    import validators

    params = {"format": "json", "url": "%s" % Iurl}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    if validators.url(Iurl):
        with urllib.request.urlopen(url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
            title = data['title']
    else:
        title = Iurl
    
    # got from https://stackoverflow.com/a/4510805
    for i, c in enumerate(title):
        if c.isdigit():
            title = title[i:i+3]
            break

    return title

def file_writing(batfile,txtfile,frows,fdic):
    if fdic[f'{frows[1]}'][1] == 0:
        batfile.write(f'start https://www.google.com/search?q={fdic[f"{frows[1]}"][0]}\n')
        for i in range(2,4):
            if not frows[i].isdigit():
                batfile.write(f'start {frows[i]}\n')

        txtfile.write(f'{frows[1]}\n{number_get(frows[2])}\n{number_get(frows[3])}\n\n')

        if frows[1] == 'Culto' or frows[1] == 'Escola Sabatina':
            if frows[4] != '':
                batfile.write(f'start {frows[4].replace("open?","uc?")}&export=download\n')
            else:
                batfile.write('\n')
           #get file name txtfile.write()

            if frows[1] == 'Escola Sabatina':
                txtfile.write(f'{frows[5]}\n\n')

        fdic[f'{frows[1]}'][1] += 1





def necfiles(dlink):
    import os.path
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from __future__ import print_function

    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
# If modifying these scopes, delete the file token.json.
    DSCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

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



# TODO objetive: clean Momento Especial
# TODO add type of doxology hymn to txt file and bat file if needed
# TODO add doxology playlist link to bat file
# TODO #7 download necessary files (bat file) and ---get their names, add names to txt file---