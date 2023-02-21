from pathlib import Path
import os
import datetime
import sys
from googleapis import googleapis
from datetools import datetools
from files import files
from VersionManager import VersionManager


CURRENT_VERSION = 1.4


def init():
    if not VersionManager.isLatestVersion(CURRENT_VERSION):
        print('[bold red]!!! NEW VERSION AVAILABLE !!!')
        os.startfile(os.path.abspath('updater.exe'))
        sys.exit()




def main():
    # ----- start of file creation -----
        # Main Working Directory
        maindir = os.path.join(Path.home(), f'Desktop\\AutoMM\\{datetools.satcalc(datetools.today,datetools.weekday)}\\')

        os.makedirs(os.path.dirname(maindir), exist_ok=True)

        dic = {
            'Momentos de Louvor':['MDL',0],
            'Culto':['C',0],
            'Escola Sabatina':['ES',0],
            'Anúncios':['AN',0],
            'Programa da Tarde':['PDT',0],
            'Momento Especial':['ME',{
                'Durante a Escola Sabatina':0,
                'Após a Escola Sabatina':0,
                'Antes do Culto':0,
                'Durante o Culto':0,
                'Após o Culto':0
            }]
        }

        # Start the bat file
        batfile = open(maindir + 'Open Me.bat','w')
        batfile.write('@echo off\n')

        # Start the txt file
        txtfile = open(maindir + f'{datetools.satcalc(datetools.today,datetools.weekday)}.txt','w')
        txtfile.write(f'Programa {datetools.satcalc(datetools.today,datetools.weekday)}\n\n')
        
        Files = files(maindir,batfile,txtfile,dic)

        for row in reversed(googleapis.sheetsapi()):
            if datetools.today <= datetime.datetime.strptime(row[0], '%d/%m/%Y'):
                getattr(Files,row[1].replace(' ','_'))(row)

if __name__ == '__main__':
    main()
input('Finished.')
