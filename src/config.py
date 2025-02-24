import yaml
from os import path
from typing import Literal

settingTypes = Literal["sheetid", "youtube"]


class Config:
    @staticmethod
    def getkeys(setting: settingTypes) -> dict[str, str | bool]:
        with open(path.abspath("config/config.yaml"), "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if setting == "sheetid":
            return config.get("ids")["spreadsheetid"]

        if setting == "youtube":
            return config.get("settings")["youtube"]

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
    def swapBool() -> None:
        with open(path.abspath("config/config.yaml"), "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if config.get("settings")["youtube"]:
            config["settings"]["youtube"] = False

            with open(path.abspath("config/config.yaml"), "w", encoding="utf-8") as f:
                config = yaml.safe_dump(config, f, default_flow_style=False)
            return

        config["settings"]["youtube"] = True
        with open(path.abspath("config/config.yaml"), "w", encoding="utf-8") as f:
            config = yaml.safe_dump(config, f, default_flow_style=False)
        return

    @staticmethod
    def getSpreadsheetID() -> None:
        with open(path.abspath("config/config.yaml"), "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        config["ids"]["spreadsheetid"] = input("Please input the Spreadsheet id: ")
        with open(path.abspath("config/config.yaml"), "w", encoding="utf-8") as f:
            config = yaml.safe_dump(config, f, default_flow_style=False)

    @staticmethod
    def verifyConfig(): ...
