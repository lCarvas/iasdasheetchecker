from pathlib import Path
from os import system
from versionmanager import VersionManager
from config import Config
from boletim import Boletim
from ui import UI

CURRENT_VERSION = 1.5


def init():
    Path("./config/").mkdir(parents=True, exist_ok=True)
    Path("./Sábados/").mkdir(parents=True, exist_ok=True)

    Config.verifyConfig()
    VersionManager.verifyUpdater()
    Boletim.verifyLinks()
    UI.mainUI(updateAvailable=VersionManager.getLatestTag() > CURRENT_VERSION)


if __name__ == "__main__":
    system("title " + "MMACP")
    init()
