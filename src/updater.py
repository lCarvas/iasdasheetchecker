from VersionManager import VersionManager
import os
from pathlib import Path

os.system("title " + "Updater")

print('Downloading...')

VersionManager.download_file()

os.startfile(Path('./MMACP.exe'))