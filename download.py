import requests


def download_file(url, filename=''):
    try:
        with requests.get(url) as req:
            with open(filename, 'wb') as f:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return filename
    except Exception as e:
        print(e)
        return None


downloadLink = 'https://github.com/lcarvas/iasdasheetchecker/releases/latest/download/MMACP.exe'

download_file(downloadLink,'MMACP.exe')