import yaml
from os import path
from typing import Literal
from dic import hymndic
from pathlib import Path

SETTING_TYPES: tuple[str, ...] = (
    "spreadsheetID",
    "doxologiaInvocacao",
    "doxologiaColeta",
    "doxologiaSaida",
    "youtubeUsage",
)

type strSettingTypes = Literal[
    "spreadsheetID",
    "doxologiaInvocacao",
    "doxologiaColeta",
    "doxologiaSaida",
]

type allSettingTypes = Literal[
    strSettingTypes,
    "youtubeUsage",
]


class Config:
    @staticmethod
    def getConfigValues(setting: allSettingTypes) -> str:
        with open(path.abspath("config/config.yaml"), "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            return config.get(setting)

    @staticmethod
    def createConfig() -> None:
        Path("./config/").mkdir(parents=True, exist_ok=True)
        with open(path.abspath("config/config.yaml"), "w", encoding="utf-8") as f:
            print("Creating config file..")

            returnDict: dict[str, str | bool] = {}

            returnDict["spreadsheetID"] = input("Please input the Spreadsheet ID: ")

            while (
                youtubeUsage := input("Do you want to use YouTube? (Y/N): ").upper()
            ) not in ["Y", "N"]:
                pass

            while (
                doxologiainvocacao := input("Hino Invocação: ").upper()
            ) not in hymndic.keys():
                pass

            while (
                doxologiacoleta := input("Hino Coleta: ").upper()
            ) not in hymndic.keys():
                pass

            while (
                doxologiasaida := input("Hino Saída: ").upper()
            ) not in hymndic.keys():
                pass

            returnDict["youtubeUsage"] = True if youtubeUsage == "Y" else False
            returnDict["doxologiaInvocacao"] = doxologiainvocacao
            returnDict["doxologiaColeta"] = doxologiacoleta
            returnDict["doxologiaSaida"] = doxologiasaida

            yaml.safe_dump(returnDict, f)

        print("Config file created.")
        input("Press Enter to continue.")

    @staticmethod
    def swapBool() -> None:
        with open(path.abspath("config/config.yaml"), "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if config.get("youtubeUsage"):
            config["youtubeUsage"] = False

            with open(path.abspath("config/config.yaml"), "w", encoding="utf-8") as f:
                config = yaml.safe_dump(config, f, default_flow_style=False)
            return

        config["youtubeUsage"] = True
        with open(path.abspath("config/config.yaml"), "w", encoding="utf-8") as f:
            config = yaml.safe_dump(config, f, default_flow_style=False)
        return

    @staticmethod
    def getNewConfigValue(setting: strSettingTypes) -> None:
        with open(path.abspath("config/config.yaml"), "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        config[setting] = input(
            "Please input the new value for this setting (leave empty to discard changes): "
        )
        if config[setting] == "":
            return
        with open(path.abspath("config/config.yaml"), "w", encoding="utf-8") as f:
            config = yaml.safe_dump(config, f, default_flow_style=False)

    @staticmethod
    def verifyConfig() -> None:
        try:
            with open(path.abspath("config/config.yaml"), "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

                for key in SETTING_TYPES:
                    if config.get(key) is None:
                        print(key)
                        raise AttributeError

        except (AttributeError, FileNotFoundError):
            print("Config file invalid or not found, creating...")
            Config.createConfig()
