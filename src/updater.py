from versionmanager import VersionManager
from os import system, startfile
from pathlib import Path

system("title " + "Updater")

print("Downloading...")

VersionManager.download_file()

startfile(Path("./MMACP.exe"))
