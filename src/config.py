import yaml
from os import path
from typing import Literal
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
        """Returns the currently set value to a config key

        Args:
            setting (allSettingTypes): Config key to get the value from
        """
        with open(path.abspath("config/config.yaml"), "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            return config.get(setting)

    @staticmethod
    def createConfig() -> None:
        """Creates a config file and prompts the user to insert the values for each config key"""
        Path("./config/").mkdir(parents=True, exist_ok=True)
        with open(path.abspath("config/config.yaml"), "w", encoding="utf-8") as f:
            print("Creating config file..")

            returnDict: dict[str, str | bool] = {}

            returnDict["spreadsheetID"] = input("Please input the Spreadsheet ID: ")

            while (
                youtubeUsage := input("Do you want to use YouTube? (Y/N): ").upper()
            ) not in ["Y", "N"]:
                pass

            doxologiainvocacao = input("Hino Invocação: ").upper()

            doxologiacoleta = input("Hino Coleta: ").upper()

            doxologiasaida = input("Hino Saída: ").upper()

            returnDict["youtubeUsage"] = True if youtubeUsage == "Y" else False
            returnDict["doxologiaInvocacao"] = doxologiainvocacao
            returnDict["doxologiaColeta"] = doxologiacoleta
            returnDict["doxologiaSaida"] = doxologiasaida

            yaml.safe_dump(returnDict, f)

        print("Config file created.")
        input("Press Enter to continue.")

    @staticmethod
    def swapBool() -> None:
        """Swaps the value of boolean config keys"""
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
        """Gets a new value for string config keys, if input is empty, leaves value unchanged

        Args:
            setting (strSettingTypes): Desired config key to change value
        """
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
        """Verifies the validity of the config file. If it does not exist, or any of the config keys is not present, creates a new config file"""
        try:
            with open(path.abspath("config/config.yaml"), "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

                for key in SETTING_TYPES:
                    if config.get(key) is None:
                        raise AttributeError

        except (AttributeError, FileNotFoundError):
            print("Config file invalid or not found, creating...")
            Config.createConfig()
