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

def hymn_file_writing(batfile,txtfile,frows):
    dic = {
        'Novo Hinário':'NV',
        'Culto':'C',
        'Escola Sabatina':'ES',
        'Momento Especial':'ME'
    }
    batfile.write(f'start https://www.google.com/search?q={dic[f"{frows[1]}"]}\nstart {frows[2]}\nstart {frows[3]}\n')
    txtfile.write(f'{frows[1]}\n{number_get(frows[2])}\n{number_get(frows[3])}\n\n')
