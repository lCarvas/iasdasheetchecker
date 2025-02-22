from typing import TextIO
from googleapis import GoogleAPIs
from dic import hymndic
from boletim import Boletim
import validators
import json
import urllib
from cleantext import clean  # type: ignore


class Files:
    @staticmethod
    def link_ver(furl: str):
        if validators.url(furl):
            return True
        else:
            return False

    # got from https://stackoverflow.com/a/52664178
    @staticmethod
    def title_get(furl: str) -> str:
        params: dict[str, str] = {"format": "json", "url": "%s" % furl}
        url = "https://www.youtube.com/oembed"
        query_string: str = urllib.parse.urlencode(params)
        url: str = url + "?" + query_string

        if Files.link_ver(furl):
            with urllib.request.urlopen(url) as response:
                response_text = response.read()
                data = json.loads(response_text.decode())
                title: str = clean(data["title"], no_emoji=True)
        else:
            title = furl

        # got from https://stackoverflow.com/a/4510805
        for i, c in enumerate(title):
            if c.isdigit():
                title = title[i : i + 3]
                break

        return title

    # ------------------------------------------------------

    def __init__(
        self,
        maindir: str,
        batfile: TextIO | None,
        txtfile: TextIO,
        dic: dict[str, str | list[str | dict[str, int]]],
        AN: int = 0,
        C: int = 0,
        ES: int = 0,
        MDL: int = 0,
        PDT: int = 0,
    ):
        self.maindir = maindir
        self.batfile = batfile
        self.txtfile = txtfile
        self.dic = dic
        self.an = AN
        self.c = C
        self.es = ES
        self.mdl = MDL
        self.pdt = PDT

    def starting(self, frow: list[str]):
        print(f"Starting {frow[1]}")
        if self.batfile is not None:
            self.batfile.write(
                f"start https://www.google.com/search?q={self.dic[f'{frow[1]}'][0]}\n"
            )
        self.txtfile.write(f"{frow[1]}\n")

    def hinos(self, frow: list[str]):
        for i in range(2, 4):
            if self.batfile is not None:
                if self.link_ver(frow[i]):
                    self.batfile.write(f"start {frow[i]}\n")
                else:
                    if frow[i] in hymndic.keys():
                        self.batfile.write(f"start {hymndic[frow[i]]}\n")

            self.txtfile.write(f"{self.title_get(frow[i])}\n\n")

    def ficheiros(self, frow: list[str]):
        try:
            if frow[4] != "":
                self.txtfile.write(f"{GoogleAPIs.driveapi(frow[4], self.maindir)}\n\n")
            else:
                self.txtfile.write("\n")
        except IndexError:
            pass

    # ------------------------------------------------------

    def Anúncios(self, frow: list[str]):
        if self.an == 0:
            self.an += 1
            self.starting(frow)
            self.ficheiros(frow)
            print()

    def Culto(self, frow: list[str]):
        if self.c == 0:
            self.c += 1
            self.starting(frow)
            self.hinos(frow)
            self.ficheiros(frow)

            # Doxologia
            if self.batfile is not None:
                self.batfile.write(
                    "start https://www.youtube.com/playlist?list=PL3sgRPOFYAyxahQy75UOv_wGlAvegskT_\n"
                )
            for j in range(7, 10):
                if frow[j] != "Normal":
                    if self.batfile is not None:
                        if self.link_ver(frow[j]):
                            self.batfile.write(f"start {frow[j]}\n")
                        else:
                            self.batfile.write(f"start {hymndic[frow[j]]}\n")
                    self.txtfile.write(f"{self.title_get(frow[j])}\n")
                else:
                    self.txtfile.write(f"{frow[j]}\n")
            self.txtfile.write("\n")
            print()

    def Escola_Sabatina(self, frow: list[str]):
        if self.es == 0:
            self.es += 1
            self.starting(frow)
            self.hinos(frow)
            self.ficheiros(frow)

            # Boletim Missionário
            if frow[6] == "Vídeo":
                Boletim.downloadboletim(self.maindir)
            print()

    def Momentos_de_Louvor(self, frow: list[str]):
        if self.mdl == 0:
            self.mdl += 1
            self.starting(frow)
            self.hinos(frow)
            self.ficheiros(frow)
            print()

    def Momento_Especial(self, frow: list[str]):
        if self.dic["Momento Especial"][1][frow[10]] == 0:
            self.dic["Momento Especial"][1][frow[10]] += 1
            self.starting(frow)
            self.ficheiros(frow)

            if self.batfile is not None:
                if frow[11] != "Não":
                    self.batfile.write(f"\nstart {frow[11]}\n")

            self.txtfile.write(f"\n{frow[10]}\n{self.title_get(frow[11])}\n\n")
            print()

    def Programa_da_Tarde(self, frow: list[str]):
        if self.pdt == 0:
            self.pdt += 1
            self.starting(frow)
            self.hinos(frow)
            self.ficheiros(frow)

            self.txtfile.write(f"{frow[5]}\n")
            print()
