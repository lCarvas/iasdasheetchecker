from pathlib import Path
import os
from funcs import *
from googleapi import *
from datetools import *
from files import *



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
            'Momento Especial':['ME',0,{
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
                getattr(Files,row[1])(row)
                # if row[1] == 'Momento Especial':
                #     pass
                #     # if dic['Momento Especial'][1] == 0:
                #     #     batfile.write(f'start https://www.google.com/search?q=ME\n')
                #     #     txtfile.write(f'{row[1]}')
                #     #     dic['Momento Especial'][1] += 1
                #     # for time in dic['Momento Especial'][2].keys():
                #     #     if time == row[10]:
                #     #         if dic['Momento Especial'][2][row[10]] == 0:
                #     #             if row[11] != 'Não':
                #     #                 batfile.write(f'\nstart {row[11]}\n')
                #     #             txtfile.write(f'\n{row[10]}\n{number_get(row[11])}\n\n')
                #     #             if row[4] != '':
                #     #                 txtfile.write(f'{necfiles(row[4],maindir,creds)}\n\n')
                #     #             else:
                #     #                 txtfile.write('\n')
                #     #             dic['Momento Especial'][2][row[10]] += 1
                #     #         else:
                #     #             pass
                # else:
                #     if row[1] == 'Culto':
                #          Files.Culto(row)


if __name__ == '__main__':
    main()
input('Finished.')
