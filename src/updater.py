from VersionManager import VersionManager
import os

os.system("title " + "Updater")

print('Downloading...')

VersionManager.download_file()

os.startfile(os.path.abspath('MMACP.exe'))