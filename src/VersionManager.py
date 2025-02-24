# got from https://raw.githubusercontent.com/LeagueOfPoro/CapsuleFarmerEvolved/master/src/VersionManager.py

import requests
from tqdm.auto import tqdm
from os import startfile, path
import sys


class VersionManager:
    @staticmethod
    def getLatestTag() -> float:
        latestTagResponse = requests.get(
            "https://api.github.com/repos/lCarvas/iasdasheetchecker/releases/latest"
        )
        if "application/json" in latestTagResponse.headers.get("Content-Type", ""):
            latestTagJson = latestTagResponse.json()
            if "tag_name" in latestTagJson:
                return float(latestTagJson["tag_name"][1:])
        return 0.0

    @staticmethod
    def getUpdate() -> None:
        startfile(path.abspath("updater.exe"))
        sys.exit()

    @staticmethod
    def download_file() -> None:
        try:
            with requests.get(
                "https://github.com/lcarvas/iasdasheetchecker/releases/latest/download/MMACP.exe"
            ) as req:
                total_length = int(req.headers.get("content-length"))
                with (
                    open("MMACP.exe", "wb") as f,
                    tqdm(
                        desc="MMACP.exe",
                        total=total_length,
                        unit="iB",
                        unit_scale=True,
                        unit_divisor=1024,
                    ) as bar,
                ):
                    for chunk in req.iter_content(chunk_size=8192):
                        if chunk:
                            bar.update(f.write(chunk))

                f.close()
                req.close()

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def download_updater() -> None:
        try:
            with requests.get(
                "https://github.com/lcarvas/iasdasheetchecker/releases/latest/download/updater.exe"
            ) as req:
                total_length = int(req.headers.get("content-length"))
                with (
                    open("updater.exe", "wb") as f,
                    tqdm(
                        desc="updater.exe",
                        total=total_length,
                        unit="iB",
                        unit_scale=True,
                        unit_divisor=1024,
                    ) as bar,
                ):
                    for chunk in req.iter_content(chunk_size=8192):
                        if chunk:
                            bar.update(f.write(chunk))

                f.close()
                req.close()

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def verifyUpdater() -> None:
        if not path.exists("./updater.exe"):
            print("Updater not found, downloading...")
            VersionManager.download_updater()
            print("Updater downloaded.")
