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
            return config.get("spreadsheetid")

        if setting == "youtube":
            return config.get("youtube")

    @staticmethod
    def createConfig() -> None:
        with open("./config/config.yaml", "w") as f:
            print("Creating config file..")

            returnDict: dict[str, str | bool] = {}

            returnDict["spreadsheetid"] = input("Please input the Spreadsheet ID: ")

            while (
                youtubeUsage := input("Do you want to use YouTube? (Y/N): ").upper()
            ) not in ["Y", "N"]:
                pass

            returnDict["youtubeUsage"] = True if youtubeUsage == "Y" else False

            yaml.safe_dump(returnDict, f)

        print("Config file created.")
        input("Press Enter to continue.")

    @staticmethod
    def swapBool() -> None:
        with open(path.abspath("config/config.yaml"), "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if config.get["youtubeUsage"]:
            config["youtubeUsage"] = False

            with open(path.abspath("config/config.yaml"), "w", encoding="utf-8") as f:
                config = yaml.safe_dump(config, f, default_flow_style=False)
            return

        config["youtubeUsage"] = True
        with open(path.abspath("config/config.yaml"), "w", encoding="utf-8") as f:
            config = yaml.safe_dump(config, f, default_flow_style=False)
        return

    @staticmethod
    def getSpreadsheetID() -> None:
        with open(path.abspath("config/config.yaml"), "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        config["spreadsheetid"] = input(
            "Please input the Spreadsheet ID (leave empty to discard changes): "
        )
        if config["spreadsheetid"] == "":
            return
        with open(path.abspath("config/config.yaml"), "w", encoding="utf-8") as f:
            config = yaml.safe_dump(config, f, default_flow_style=False)

    @staticmethod
    def verifyConfig():
        try:
            with open(path.abspath("config/config.yaml"), "r") as f:
                config = yaml.safe_load(f)

                for key in [
                    "spreadsheetid",
                    "youtubeusage",
                ]:
                    if config.get(key) is None:
                        raise AttributeError

        except AttributeError or FileNotFoundError:
            print("Config file invalid or not found, creating...")
            Config.createConfig()
