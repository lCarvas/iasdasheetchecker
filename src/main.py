from pathlib import Path
import os
import datetime
import time
import sys
from googleapis import googleapis
from datetools import datetools
from files import files
from VersionManager import VersionManager
from config import Config
from boletim import boletim


CURRENT_VERSION = 1.4


def init():
    Path("./config/").mkdir(parents=True, exist_ok=True)
    Path("./Sábados/").mkdir(parents=True, exist_ok=True)

    if not os.path.exists('./config/config.yaml'):
        print('Config file not found, creating...')
        with open('./config/config.yaml', 'w') as f:
             f.write('ids:\n spreadsheetid:\n drivefolderid:')
             f.close()
        print('Config file created, please fill it in and reopen the app.')
        input('Press Enter to close the app.')
        sys.exit()

    if not os.path.exists('./updater.exe'):
        print('Updater not found, downloading...')
        VersionManager.download_updater()
        print('Updater downloaded.')

    if not os.path.exists('./config/links.yaml') or datetools.today > datetime.datetime.strptime(boletim.checkfinaldate(),'%d-%m-%Y'):
        print('Links Boletim Missionário not found, creating...')
        boletim.linksyaml()
        print('Links file created.')

    if None in Config.getkeys().values():
        print('Config file not filled in properly, did you correctly put both keys in?')
        input('Press Enter to close the app.')
        sys.exit()


    if not VersionManager.isLatestVersion(CURRENT_VERSION):
        print('[bold red]!!! NEW VERSION AVAILABLE !!!')
        print('Downloading...')
        time.sleep(1)
        os.startfile(os.path.abspath('updater.exe'))
        sys.exit()


def main():
    # ----- start of file creation -----
    # Main Working Directory
    maindir = f'./Sábados/{datetools.satcalc(datetools.today,datetools.weekday)}/'
    os.makedirs(os.path.dirname(maindir), exist_ok=True)

    dic = {
        'Anúncios':['AN',0],
        'Culto':['C',0],
        'Escola Sabatina':['ES',0],
        'Momentos de Louvor':['MDL',0],
        'Momento Especial':['ME',{
            'Durante a Escola Sabatina':0,
            'Após a Escola Sabatina':0,
            'Antes do Culto':0,
            'Durante o Culto':0,
            'Após o Culto':0
        }],
        'Programa da Tarde':['PDT',0]
    }

    # Start the bat file
    batfile = open(maindir + 'Open Me.bat','w')
    batfile.write('@echo off\n')

    # Start the txt file
    txtfile = open(maindir + f'{datetools.satcalc(datetools.today,datetools.weekday)}.txt','w')
    txtfile.write(f'Programa {datetools.satcalc(datetools.today,datetools.weekday)}\n\n')
    
    Files = files(maindir,batfile,txtfile,dic)

    googleapis.SPREADSHEET_ID = Config.getkeys()['spreadsheetid']
    googleapis.DRIVEFOLDER_ID = Config.getkeys()['driveid']


    for row in reversed(googleapis.sheetsapi()):
        if datetools.today <= datetime.datetime.strptime(row[0], '%d/%m/%Y'):
            getattr(Files,row[1].replace(' ','_'))(row)
    
    txtfile.close()
    batfile.close()

if __name__ == '__main__':
    os.system("title " + "MMACP")
    init()
    main()
    input('Finished.\nPress Enter to close the app.')