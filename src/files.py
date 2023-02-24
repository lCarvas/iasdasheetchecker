from googleapis import googleapis
from dic import hymndic
from boletim import boletim


class files:
    @staticmethod
    def link_ver(furl):
        import validators

        if validators.url(furl):
            return True
        else:
            return False
        

    # got from https://stackoverflow.com/a/52664178
    @staticmethod
    def title_get(furl):
        import urllib.request
        import json
        import urllib
        from cleantext import clean

        params = {"format": "json", "url": "%s" % furl}
        url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        url = url + "?" + query_string

        if files.link_ver(furl):
            with urllib.request.urlopen(url) as response:
                response_text = response.read()
                data = json.loads(response_text.decode())
                title = clean(data['title'], no_emoji=True)
        else:
            title = furl
        
        # got from https://stackoverflow.com/a/4510805
        for i, c in enumerate(title):
            if c.isdigit():
                title = title[i:i+3]
                break

        return title
    
#------------------------------------------------------

    def __init__(self,maindir,batfile,txtfile,dic):
        self.maindir = maindir
        self.batfile = batfile
        self.txtfile = txtfile        
        self.dic = dic

    def starting(self,frow):
        print(f'Starting {frow[1]}')
        self.batfile.write(f'start https://www.google.com/search?q={self.dic[f"{frow[1]}"][0]}\n')
        self.txtfile.write(f'{frow[1]}\n')

    def hinos(self,frow):
        for i in range(2,4):
            if self.link_ver(frow[i]):
                self.batfile.write(f'start {frow[i]}\n')
            else:
                if frow[i] in hymndic.keys():
                    self.batfile.write(f'start {hymndic[frow[i]]}\n')

            self.txtfile.write(f'{self.title_get(frow[i])}\n\n')

    def ficheiros(self,frow):
        try:
            if frow[4] != '':
                self.txtfile.write(f'{googleapis.driveapi(frow[4],self.maindir)}\n\n')
            else:
                self.txtfile.write('\n')
        except IndexError:
            pass

#------------------------------------------------------

    def Anúncios(self,frow):
        if self.dic[f'{frow[1]}'][1] == 0:
            self.dic[f'{frow[1]}'][1] += 1
            self.starting(frow)
            self.ficheiros(frow)
            print()

    def Culto(self,frow):
        if self.dic[f'{frow[1]}'][1] == 0:
            self.dic[f'{frow[1]}'][1] += 1
            self.starting(frow)
            self.hinos(frow)
            self.ficheiros(frow)

            # Doxologia
            self.batfile.write(f'start https://www.youtube.com/playlist?list=PL3sgRPOFYAyxahQy75UOv_wGlAvegskT_\n')
            for j in range(7,10):
                if frow[j] != 'Normal':
                    if self.link_ver(frow[j]):
                        self.batfile.write(f'start {frow[j]}\n')
                    else:
                        self.batfile.write(f'start {hymndic[frow[j]]}\n')
                    self.txtfile.write(f'{self.title_get(frow[j])}\n')
                else:
                    self.txtfile.write(f'{frow[j]}\n')
            self.txtfile.write('\n')
            print()

    def Escola_Sabatina(self,frow):
        if self.dic[f'{frow[1]}'][1] == 0:
            self.dic[f'{frow[1]}'][1] += 1
            self.starting(frow)
            self.hinos(frow)
            self.ficheiros(frow)
            
            # Boletim Missionário
            if frow[6] == 'Vídeo':
                boletim.downloadboletim()
            print()
    
    def Momentos_de_Louvor(self,frow):
        if self.dic[f'{frow[1]}'][1] == 0:
            self.dic[f'{frow[1]}'][1] += 1
            self.starting(frow)
            self.hinos(frow)
            self.ficheiros(frow)
            print()
    
    def Momento_Especial(self,frow):
        if self.dic['Momento Especial'][1][frow[10]] == 0:
            self.dic['Momento Especial'][1][frow[10]] += 1
            self.starting(frow)
            self.ficheiros(frow)

            if frow[11] != 'Não':
                self.batfile.write(f'\nstart {frow[11]}\n')

            self.txtfile.write(f'\n{frow[10]}\n{self.title_get(frow[11])}\n\n')
            print()

    def Programa_da_Tarde(self,frow):
        if self.dic[f'{frow[1]}'][1] == 0:
            self.dic[f'{frow[1]}'][1] += 1
            self.starting(frow)
            self.hinos(frow)
            self.ficheiros(frow)

            self.txtfile.write(f'{frow[5]}\n')
            print()