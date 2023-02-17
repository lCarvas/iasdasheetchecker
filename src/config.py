import yaml
from yaml.parser import ParserError
import os

class Config:
    @staticmethod
    def getkeys():
        with open(os.path.abspath('config/config.yaml'),'r',encoding='utf-8' ) as f:
            config = yaml.safe_load(f)
            apikeys = {
                'spreadsheetid': config.get("ids")['spreadsheetid'],
                'driveid': config.get("ids")['drivefolderid']
            }
        return apikeys