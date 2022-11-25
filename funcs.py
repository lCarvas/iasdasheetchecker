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



# TODO objetive: clean Momento Especial 
