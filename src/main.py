from pathlib import Path
import os
from funcs import *

# Main Working Directory
maindir = os.path.join(Path.home(), f'Desktop\\AutoMM\\{satcalc(today,weekday)}\\')


def main():

    # ----- start of file creation -----

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
        txtfile = open(maindir + f'{satcalc(today,weekday)}.txt','w')
        txtfile.write(f'Programa {satcalc(today,weekday)}\n\n')

    #TODO Adicionar auto video carta missionaria at some point
        for row in reversed(values):
            if today <= datetime.datetime.strptime(row[0], '%d/%m/%Y'):
                if row[1] == 'Momento Especial':
                    if dic['Momento Especial'][1] == 0:
                        batfile.write(f'start https://www.google.com/search?q=ME\n')
                        txtfile.write(f'{row[1]}')
                        dic['Momento Especial'][1] += 1
                    for time in dic['Momento Especial'][2].keys():
                        if time == row[10]:
                            if dic['Momento Especial'][2][row[10]] == 0:
                                if row[11] != 'Não':
                                    batfile.write(f'\nstart {row[11]}\n')
                                txtfile.write(f'\n{row[10]}\n{number_get(row[11])}\n\n')
                                if row[4] != '':
                                    txtfile.write(f'{necfiles(row[4],maindir,creds)}\n\n')
                                else:
                                    txtfile.write('\n')
                                dic['Momento Especial'][2][row[10]] += 1
                            else:
                                pass
                else:
                    file_writing(batfile,txtfile,row,dic,maindir,creds)


if __name__ == '__main__':
    main()
input('Finished.')
