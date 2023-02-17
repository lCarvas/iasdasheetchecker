import requests
from bs4 import BeautifulSoup


r = requests.get('https://recursos.adventistas.org.pt/escolasabatina/videos/boletim-missionario-1-o-trimestre-de-2023/').content
soup = BeautifulSoup(r, features="html.parser")
mc = soup.find('div', attrs={'class':'mb-5'})
content = mc.find('tr')
print(content)



# with requests.get(r"https://s3.eu-central-003.backblazeb2.com/upasd-recursos/escola-sabatina/boletim-missionario/2023/1T/28%20de%20janeiro%20-%20O%20Livro%20que%20a%20Bicicleta%20Trouxe.mp4") as req:
#     with open('boletim.mp4','wb') as f:
#         for chunk in req.iter_content(chunk_size=8192):
#             f.write(chunk)
