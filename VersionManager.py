# got from https://raw.githubusercontent.com/LeagueOfPoro/CapsuleFarmerEvolved/master/src/VersionManager.py 

import requests

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

