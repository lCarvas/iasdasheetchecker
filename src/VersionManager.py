# got from https://raw.githubusercontent.com/LeagueOfPoro/CapsuleFarmerEvolved/master/src/VersionManager.py 

import requests
from tqdm.auto import tqdm

class VersionManager:

    @staticmethod
    def getLatestTag():
        latestTagResponse = requests.get("https://api.github.com/repos/lCarvas/iasdasheetchecker/releases/latest")
        if 'application/json' in latestTagResponse.headers.get('Content-Type', ''):
            latestTagJson = latestTagResponse.json()
            if "tag_name" in latestTagJson:
                return float(latestTagJson["tag_name"][1:])
        return 0.0
    
    @staticmethod
    def isLatestVersion(currentVersion):
        return currentVersion >= VersionManager.getLatestTag()
    
    @staticmethod
    def download_file():
        try:
            with requests.get('https://github.com/lcarvas/iasdasheetchecker/releases/latest/download/MMACP.exe') as req:
                total_length = int(req.headers.get('content-length'))
                with open('MMACP.exe', 'wb') as f, tqdm(desc='MMACP.exe', total=total_length,unit='iB',unit_scale=True,unit_divisor=1024) as bar:
                    for chunk in req.iter_content(chunk_size=8192):
                        if chunk:
                            bar.update(f.write(chunk))
        except Exception as e:
            print(e)
            return None
        
    @staticmethod
    def download_updater():
        try:
            with requests.get('https://github.com/lcarvas/iasdasheetchecker/releases/latest/download/updater.exe') as req:
                total_length = int(req.headers.get('content-length'))
                with open('updater.exe', 'wb') as f, tqdm(desc='updater.exe', total=total_length,unit='iB',unit_scale=True,unit_divisor=1024) as bar:
                    for chunk in req.iter_content(chunk_size=8192):
                        if chunk:
                            bar.update(f.write(chunk))
        except Exception as e:
            print(e)
            return None