from bs4.element import NavigableString, PageElement
import requests
from bs4 import BeautifulSoup, Tag
import yaml
from os import path
from datetools import DateTools
from tqdm.auto import tqdm
from datetime import datetime
from typing import Any


class Boletim:
    @staticmethod
    def getlinklist() -> list[Any]:
        """Returns a list of links from the boletim website relevant to the current trimester and year"""
        linklist: list[Any] = []
        r: bytes | Any = requests.get(
            "https://recursos.adventistas.org.pt/escolasabatina/videos/boletim-missionario-{}-o-trimestre-de-{}/".format(
                DateTools.trim, DateTools.today.year
            )
        ).content
        soup = BeautifulSoup(r, "html.parser")
        mc: PageElement | Tag | NavigableString | None = soup.find(
            "div", attrs={"class": "mb-5"}
        )
        for link in mc.find_all("a"):
            linklist.append(link.get("href"))

        if ".pdf" in linklist[0]:
            linklist.pop(0)
        linklist = linklist[1::2]

        return linklist

    @staticmethod
    def linksyaml() -> None:
        """Creates/Updates a yaml file whose keys are the dates corresponding to the values that are the boletim download links relevant to the current year and trimester and"""
        yamllist = dict(zip(DateTools.trimsat(), Boletim.getlinklist()))
        with open(path.abspath("config/links.yaml"), "w", encoding="utf-8") as f:
            yaml.safe_dump(yamllist, f, sort_keys=False)

    @staticmethod
    def downloadboletim(fmaindir: str):
        """Downloads the relevant boletim correspondent to the closest saturday

        Args:
            fmaindir (str): Working directory
        """
        with open(path.abspath("config/links.yaml"), "r", encoding="utf-8") as f:
            links = yaml.safe_load(f)

        with requests.get(
            links.get(str(DateTools.satcalc(DateTools.today))), stream=True
        ) as req:
            total_length = int(req.headers.get("content-length"))
            with (
                open(f"{fmaindir}/Boletim.mp4", "wb") as f,
                tqdm(
                    desc="Boletim.mp4",
                    total=total_length,
                    unit="iB",
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar,
            ):
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        bar.update(f.write(chunk))

    @staticmethod
    def checkfinaldate() -> str:
        """Returns the last date present on the yaml files"""
        with open(path.abspath("config/links.yaml"), "r", encoding="utf-8") as f:
            links: dict[str, str] = yaml.safe_load(f)
            finaldate: str = list(links.keys())[-1]
        return finaldate

    @staticmethod
    def verifyLinks() -> None:
        """Verifies the validity of the links yaml file, if the files does not exist or the current date is past the last date present on the file, requests a new links yaml file"""
        if (
            not path.exists("./config/links.yaml")
            or DateTools.satcalc(DateTools.today)
            > datetime.strptime(Boletim.checkfinaldate(), "%Y-%m-%d").date()
        ):
            print("Links Boletim Missionário not found, creating...")
            Boletim.linksyaml()
            print("Links file created.")
