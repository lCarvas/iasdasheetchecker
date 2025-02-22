from pathlib import Path
from os import system
from datetime import datetime
from googleapis import GoogleAPIs
from datetools import DateTools
from files import Files
from VersionManager import VersionManager
from config import Config
from boletim import Boletim
from typing import TextIO


CURRENT_VERSION = 1.45


def init():
    Path("./config/").mkdir(parents=True, exist_ok=True)
    Path("./Sábados/").mkdir(parents=True, exist_ok=True)

    Config.firstTimeSetup()
    VersionManager.verifyUpdater()
    Boletim.verifyLinks()
    VersionManager.getUpdate(CURRENT_VERSION)

    # if None in Config.getkeys("sheetid").values():
    #     print("Config file not filled in properly, did you put the key in correctly?")
    #     input("Press Enter to close the app.")
    #     sys.exit()


def main() -> None:
    # ----- start of file creation -----
    dic: dict[str, str | list[str | dict[str, int]]] = {
        "Anúncios": "AN",
        "Culto": "C",
        "Escola Sabatina": "ES",
        "Momentos de Louvor": "MDL",
        "Momento Especial": [
            "ME",
            {
                "Durante a Escola Sabatina": 0,
                "Após a Escola Sabatina": 0,
                "Antes do Culto (Após os Anúncios)": 0,
                "Durante o Culto": 0,
                "Após o Culto": 0,
            },
        ],
        "Programa da Tarde": "PDT",
    }

    GoogleAPIs.SPREADSHEET_ID = Config.getkeys("sheetid")["spreadsheetid"]

    if (
        DateTools.today
        <= datetime.strptime(GoogleAPIs.sheetsapi()[-1][0], "%d/%m/%Y").date()
    ):
        # Main Working Directory
        maindir: str = f"./Sábados/{DateTools.satcalc(DateTools.today)}/"
        # Path(path.dirname(maindir).mkdir(exist_ok=True))
        Path(maindir).mkdir(exist_ok=True)

        # Start the txt file
        txtfile: TextIO = open(
            maindir + f"{DateTools.satcalc(DateTools.today)}.txt", "w"
        )
        txtfile.write(f"Programa {DateTools.satcalc(DateTools.today)}\n\n")

        # Start the bat file
        batfile: TextIO | None = None
        if Config.getkeys("youtube"):
            batfile = open(maindir + "Open Me.bat", "w")
            batfile.write("@echo off\n")

        files = Files(maindir, batfile, txtfile, dic)

        for row in reversed(GoogleAPIs.sheetsapi()):
            if DateTools.today <= datetime.strptime(row[0], "%d/%m/%Y").date():
                getattr(files, row[1].replace(" ", "_"))(row)

        txtfile.close()
        if batfile is not None:
            batfile.close()


if __name__ == "__main__":
    system("title " + "MMACP")
    init()
    main()
    input("Finished.\nPress Enter to close the app.")
