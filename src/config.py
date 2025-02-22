import yaml
import os
from typing import Literal

settingTypes = Literal["sheetid", "youtube"]


class Config:
    @staticmethod
    def getkeys(setting: settingTypes):
        with open(os.path.abspath("config/config.yaml"), "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

            if setting == "sheetid":
                apikeys = {
                    "spreadsheetid": config.get("ids")["spreadsheetid"],
                }
                return apikeys

            if setting == "youtube":
                return {"youtubekey": config.get("youtube")}
