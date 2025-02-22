import yaml
from os import path
from typing import Literal

settingTypes = Literal["sheetid", "youtube"]


class Config:
    @staticmethod
    def getkeys(setting: settingTypes):
        with open(path.abspath("config/config.yaml"), "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

            if setting == "sheetid":
                apikeys = {
                    "spreadsheetid": config.get("ids")["spreadsheetid"],
                }
                return apikeys

            if setting == "youtube":
                return {"youtubekey": config.get("youtube")}

    @staticmethod
    def firstTimeSetup() -> None:
        if not path.exists("./config/config.yaml"):
            print("Config file not found, creating...")
            with open("./config/config.yaml", "w") as f:
                print("Running first time setup..")
                sheetid: str = input("Please input the Spreadsheet id: ")
                while (
                    youtubeUsage := input("Do you want to use YouTube? (Y/N): ").upper()
                ) not in ["Y", "N"]:
                    pass
                f.write(
                    f"ids:\n  spreadsheetid: {sheetid}\nsettings:\n  youtube: {True if youtubeUsage.upper() == 'Y' else False}"
                )
            f.close()
            print("Config file created.")
            print("Please place the credentials file inside the config folder.")
            input(
                "Press Enter after you put the credentials file inside the config folder."
            )

    @staticmethod
    def verifyConfig(): ...
