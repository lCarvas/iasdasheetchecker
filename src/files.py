from datetime import datetime
from googleapis import GoogleAPIs
from datetools import DateTools
from typing import TextIO
from dic import hymndic
from boletim import Boletim
from config import Config
from pathlib import Path
import validators
import json
import urllib
from cleantext import clean


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

    def starting(self, valuesDict: dict[str, list[str]], index: int):
        print(f"Starting {valuesDict['Tipo de Formulário'][index]}")
        if self.batfile is not None:
            self.batfile.write(
                f"start https://www.google.com/search?q={self.dic[f'{valuesDict["Tipo de Formulário"][index]}'][0]}\n"
            )
        self.txtfile.write(f"{valuesDict['Tipo de Formulário'][index]}\n")

    def hinos(self, valuesDict: dict[str, list[str]], index: int):
        for item in ("1° Hino", "2° Hino"):
            if self.batfile is not None:
                if self.link_ver(valuesDict[item][index]):
                    self.batfile.write(f"start {valuesDict[item][index]}\n")
                else:
                    if valuesDict[item][index] in hymndic.keys():
                        self.batfile.write(
                            f"start {hymndic[valuesDict[item][index]]}\n"
                        )
            self.txtfile.write(f"{item}: {self.title_get(valuesDict[item][index])}\n")

        self.txtfile.write("\n")

    def ficheiros(self, valuesDict: dict[str, list[str]], index: int):
        try:
            if valuesDict["Ficheiros Necessários"][index] != "":
                self.txtfile.write(
                    f"{GoogleAPIs.driveapi(valuesDict['Ficheiros Necessários'][index], self.maindir)}\n\n"
                )
        except IndexError:
            pass

    # ------------------------------------------------------

    def Anúncios(self, valuesDict: dict[str, list[str]], index: int):
        if self.an == 0:
            self.an += 1
            self.starting(valuesDict, index)
            self.ficheiros(valuesDict, index)
            print()

    def Culto(self, valuesDict: dict[str, list[str]], index: int):
        if self.c == 0:
            self.c += 1
            self.starting(valuesDict, index)
            self.hinos(valuesDict, index)

            for item in ("Hino Invocação", "Hino Coleta", "Hino Saída"):
                match (item, valuesDict[item][index]):
                    case ("Hino Invocação", "Normal"):
                        hNum = Config.getConfigValues("doxologiaInvocacao")
                        if self.batfile is not None:
                            self.batfile.write(f"start {hymndic[hNum]}")
                        self.txtfile.write(f"{item}: {hNum}\n")

                    case ("Hino Invocação", _):
                        if self.batfile is not None:
                            if self.link_ver(valuesDict[item][index]):
                                self.batfile.write(f"start {valuesDict[item][index]}\n")
                            else:
                                self.batfile.write(
                                    f"start {hymndic[valuesDict[item][index]]}\n"
                                )
                        self.txtfile.write(
                            f"{item}: {self.title_get(valuesDict[item][index])}\n"
                        )

                    case ("Hino Coleta", "Normal"):
                        hNum = Config.getConfigValues("doxologiaColeta")
                        if self.batfile is not None:
                            self.batfile.write(f"start {hymndic[hNum]}")
                        self.txtfile.write(f"{item}: {hNum}\n")

                    case ("Hino Coleta", _):
                        if self.batfile is not None:
                            if self.link_ver(valuesDict[item][index]):
                                self.batfile.write(f"start {valuesDict[item][index]}\n")
                            else:
                                self.batfile.write(
                                    f"start {hymndic[valuesDict[item][index]]}\n"
                                )
                        self.txtfile.write(
                            f"{item}: {self.title_get(valuesDict[item][index])}\n"
                        )

                    case ("Hino Saída", "Normal"):
                        hNum = Config.getConfigValues("doxologiaSaida")
                        if self.batfile is not None:
                            self.batfile.write(f"start {hymndic[hNum]}")
                        self.txtfile.write(f"{item}: {hNum}\n")

                    case ("Hino Saída", _):
                        if self.batfile is not None:
                            if self.link_ver(valuesDict[item][index]):
                                self.batfile.write(f"start {valuesDict[item][index]}\n")
                            else:
                                self.batfile.write(
                                    f"start {hymndic[valuesDict[item][index]]}\n"
                                )
                        self.txtfile.write(
                            f"{item}: {self.title_get(valuesDict[item][index])}\n"
                        )

            self.txtfile.write("\n")
            self.ficheiros(valuesDict, index)
            print()

    def Escola_Sabatina(self, valuesDict: dict[str, list[str]], index: int):
        if self.es == 0:
            self.es += 1
            self.starting(valuesDict, index)
            self.hinos(valuesDict, index)
            self.ficheiros(valuesDict, index)

            # Boletim Missionário
            if valuesDict["Carta Missionária"][index] == "Vídeo":
                Boletim.downloadboletim(self.maindir)
            print()

    def Momentos_de_Louvor(self, valuesDict: dict[str, list[str]], index: int):
        if self.mdl == 0:
            self.mdl += 1
            self.starting(valuesDict, index)
            self.hinos(valuesDict, index)
            self.ficheiros(valuesDict, index)
            print()

    def Momento_Especial(self, valuesDict: dict[str, list[str]], index: int):
        if (
            self.dic["Momento Especial"][1][
                valuesDict["Quando irá decorrer o Momento Especial?"][index]
            ]
            == 0
        ):
            self.dic["Momento Especial"][1][
                valuesDict["Quando irá decorrer o Momento Especial?"][index]
            ] += 1
            self.starting(valuesDict, index)
            self.ficheiros(valuesDict, index)

            if self.batfile is not None:
                if valuesDict["Será necessária música?"][index] != "Não":
                    self.batfile.write(
                        f"\nstart {valuesDict['Será necessária música?'][index]}\n"
                    )

            self.txtfile.write(
                f"\n{valuesDict['Quando irá decorrer o Momento Especial?'][index]}\n{self.title_get(valuesDict['Será necessária música?'][index])}\n\n"
            )
            print()

    def Programa_da_Tarde(self, valuesDict: dict[str, list[str]], index: int):
        if self.pdt == 0:
            self.pdt += 1
            self.starting(valuesDict, index)
            self.hinos(valuesDict, index)
            self.ficheiros(valuesDict, index)

            self.txtfile.write(f"{valuesDict['Programa'][index]}\n")
            print()

    def filesMain() -> None:
        # ----- start of file creation -----
        dic: dict[str, str | list[str | dict[str, int]]] = {
            "Anúncios": "AN",
            "Culto": "C",
            "Escola Sabatina": "ES",
            "Momentos de Louvor": "MDL",
            "Momento Especial": [
                "ME",
                {
                    "Durante a Escola Sabatina": 0,
                    "Após a Escola Sabatina": 0,
                    "Antes do Culto (Após os Anúncios)": 0,
                    "Durante o Culto": 0,
                    "Após o Culto": 0,
                },
            ],
            "Programa da Tarde": "PDT",
        }

        Path("./Sábados/").mkdir(parents=True, exist_ok=True)

        GoogleAPIs.SPREADSHEET_ID = Config.getConfigValues("spreadsheetID")

        sheetsResult = GoogleAPIs.sheetsapi()

        valuesDict = {
            str(sheetsResult[0][i]): [
                [
                    sheetsResult[j][i] if i < len(sheetsResult[j]) else ""
                    for j in range(len(sheetsResult) - 1, 0, -1)
                ]
                for i in range(len(sheetsResult[0]))
            ][i]
            for i in range(len(sheetsResult[0]))
        }

        if (
            DateTools.today
            <= datetime.strptime(valuesDict["Sábado"][0], "%d/%m/%Y").date()
        ):
            # Main Working Directory
            maindir: str = f"./Sábados/{DateTools.satcalc(DateTools.today)}/"
            # Path(path.dirname(maindir).mkdir(exist_ok=True))
            Path(maindir).mkdir(exist_ok=True)

            # Start the txt file
            txtfile: TextIO = open(
                maindir + f"{DateTools.satcalc(DateTools.today)}.txt",
                "w",
                encoding="utf-8",
            )
            txtfile.write(f"Programa {DateTools.satcalc(DateTools.today)}\n\n")

            # Start the bat file
            batfile: TextIO | None = None
            if Config.getConfigValues("youtubeUsage"):
                batfile = open(maindir + "Open Me.bat", "w")
                batfile.write("@echo off\n")

            files = Files(maindir, batfile, txtfile, dic)

            for index, value in enumerate(valuesDict["Sábado"]):
                if DateTools.today >= datetime.strptime(value, "%d/%m/%Y").date():
                    break

                getattr(
                    files, valuesDict["Tipo de Formulário"][index].replace(" ", "_")
                )(valuesDict, index)

            txtfile.close()
            if batfile is not None:
                batfile.close()

            input("Finished.\nPress Enter to return to the menu.")
            return

        input("Nothing found.\nPress Enter to return to the menu.")
