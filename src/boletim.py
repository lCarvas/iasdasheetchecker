import requests
from bs4 import BeautifulSoup
import yaml
import os
from datetools import datetools
from tqdm.auto import tqdm

class boletim:

    @staticmethod
    def getlinklist():
        linklist = []
        r = requests.get('https://recursos.adventistas.org.pt/escolasabatina/videos/boletim-missionario-1-o-trimestre-de-2023/').content
        soup = BeautifulSoup(r, "html.parser")
        mc = soup.find('div', attrs={'class':'mb-5'})
        for link in mc.find_all('a'):
            linklist.append(link.get('href'))

        linklist.pop()
        linklist.reverse()
        
        return linklist
    
    @staticmethod
    def linksyaml():
        yamllist = dict(zip(datetools.trimsat(), boletim.getlinklist()))
        with open(os.path.abspath('config/links.yaml'),'w') as f:
            yaml.dump(yamllist,f,sort_keys=False)

        f.close()

    @staticmethod
    def downloadboletim():
        with open(os.path.abspath('config/links.yaml'),'r',encoding='utf-8') as f:
            links = yaml.safe_load(f)

        with requests.get(links.get(datetools.satcalc(datetools.today,datetools.weekday)),stream=True) as req:
            total_length = int(req.headers.get('content-length'))
            with open('Boletim.mp4','wb') as f, tqdm(desc='Boletim.mp4', total=total_length,unit='iB',unit_scale=True,unit_divisor=1024) as bar:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        bar.update(f.write(chunk))

        f.close()

    @staticmethod
    def checkfinaldate():
        try:
            with open(os.path.abspath('config/links.yaml'),'r',encoding='utf-8') as f:
                links = yaml.safe_load(f)
                finaldate = list(links.keys())[0]
            
            f.close()
            return finaldate
        
        except FileNotFoundError:
            pass