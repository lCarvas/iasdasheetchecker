import os
from pathlib import Path
from datetools import datetools
from googleapi import googleapis
from dic import hymndic
from funcs import *

class files:
    table = googleapis.sheetsapi()

    def __init__(self,maindir,batfile,txtfile,dic):
        self.maindir = maindir
        self.batfile = batfile
        self.txtfile = txtfile        
        self.dic = dic

    def general(self,frow):
        print(f'Starting {frow[1]}')
        self.batfile.write(f'start https://www.google.com/search?q={self.dic[f"{frow[1]}"][0]}\n')
        self.txtfile.write(f'{frow[1]}\n')

    def hinos(self,frow):
        for i in range(2,4):
            if link_ver(frow[i]):
                self.batfile.write(f'start {frow[i]}\n')
            else:
                if frow[i] in hymndic.keys():
                    self.batfile.write(f'start {hymndic[frow[i]]}\n')

        self.txtfile.write(f'{number_get(frow[2])}\n{number_get(frow[3])}\n\n')


    def Culto(self,frow):
        files.hinos(self,frow)
        self.batfile.write(f'start https://www.youtube.com/playlist?list=PL3sgRPOFYAyxahQy75UOv_wGlAvegskT_\n')
        for j in range(7,10):
            if frow[j] != 'Normal':
                if link_ver(frow[j]):
                    self.batfile.write(f'start {frow[j]}\n')
                else:
                    self.batfile.write(f'start {hymndic[frow[j]]}\n')
                self.txtfile.write(f'{number_get(frow[j])}\n')
            else:
                self.txtfile.write(f'{frow[j]}\n')
        self.txtfile.write('\n')
        try:
            # Ficheiros Necessários
            if frow[4] != '':
                self.txtfile.write(f'{googleapis.driveapi(frow[4],self.maindir)}\n\n')
            else:
                self.txtfile.write('\n')
        except IndexError:
            pass