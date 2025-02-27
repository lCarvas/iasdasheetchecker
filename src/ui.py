from os import system, name, startfile, path
from queue import Queue
from pynput.keyboard import Listener
from versionmanager import VersionManager
from config import Config, SETTING_TYPES
from win32gui import GetWindowText, GetForegroundWindow
from files import Files
import msvcrt
from time import sleep
from sys import exit

keyPressReturnValue = Queue()


class UI:
    @staticmethod
    def on_press(key, config: bool, updateAvailable: bool) -> None:
        if GetWindowText(GetForegroundWindow()) in [
            "MMACP",
            "main.py - iasdasheetchecker - Visual Studio Code",
        ]:
            try:
                if not config:
                    if key.char == "1":
                        keyPressReturnValue.put("runMain")
                        return False

                    if key.char == "2":
                        keyPressReturnValue.put("openFolder")
                        return False

                    # Check Settings
                    if key.char == "3":
                        keyPressReturnValue.put("getConfig")
                        return False

                    # Update if available
                    if updateAvailable:
                        if key.char == "4":
                            keyPressReturnValue.put("getUpdate")
                            return False

                    if key.char == "0":
                        keyPressReturnValue.put("exit")
                        return False

                else:
                    if key.char == "1":
                        keyPressReturnValue.put("spreadsheetID")
                        return False

                    if key.char == "2":
                        keyPressReturnValue.put("swapBool")
                        return False

                    if key.char == "3":
                        keyPressReturnValue.put("doxologiaInvocacao")
                        return False

                    if key.char == "4":
                        keyPressReturnValue.put("doxologiaColeta")
                        return False

                    if key.char == "5":
                        keyPressReturnValue.put("doxologiaSaida")
                        return False

                    if key.char == "0":
                        keyPressReturnValue.put("returnMenu")
                        return False

            except AttributeError:
                pass

    @staticmethod
    def UIInteraction(config: bool, updateAvailable: bool) -> None:
        with Listener(
            on_press=lambda event: UI.on_press(event, config, updateAvailable),
        ) as listener:
            listener.join()

    @staticmethod
    def menuUI(updateAvailable: bool) -> None:
        system("cls" if name == "nt" else "clear")
        print(
            "\n███╗   ███╗███╗   ███╗ █████╗  ██████╗██████╗\n████╗ ████║████╗ ████║██╔══██╗██╔════╝██╔══██╗\n██╔████╔██║██╔████╔██║███████║██║     ██████╔╝\n██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║     ██╔═══╝\n██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║╚██████╗██║\n╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝\n\n"
        )

        if updateAvailable:
            print(
                "[1] Run\n[2] Open Folder\n[3] Settings\n[4] \033[31mUpdate Available!\033[0m\n[0] Exit"
            )
            UI.UIInteraction(False, updateAvailable)
            return

        print(
            "[1] Run\n[2] Open Folder\n[3] Settings\n[4] No Update Available\n[0] Exit"
        )
        UI.UIInteraction(False, updateAvailable)

    @staticmethod
    def configUI(updateAvailable: bool) -> None:
        system("cls" if name == "nt" else "clear")
        print(
            "\n███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗\n██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝\n███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗\n╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║\n███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║\n╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝\n\n"
        )
        print(f"[1] Spreadsheet ID: {Config.getConfigValues('spreadsheetID')}")
        print(f"[2] YouTube Usage: {Config.getConfigValues('youtubeUsage')}")
        print(f"[3] Hino de Invocação: {Config.getConfigValues('doxologiaInvocacao')}")
        print(f"[4] Hino de Coleta: {Config.getConfigValues('doxologiaColeta')}")
        print(f"[5] Hino de Saída: {Config.getConfigValues('doxologiaSaida')}")
        print("[0] Return")
        UI.UIInteraction(True, updateAvailable)

    def mainUI(updateAvailable: bool) -> None:
        UI.menuUI(updateAvailable)
        while True:
            returnValue: str = keyPressReturnValue.get()

            if not msvcrt.kbhit():  # if there's nothing in the buffer wait
                sleep(0.01)

            while msvcrt.kbhit():
                msvcrt.getch()

            match returnValue:
                case "runMain":
                    Files.filesMain()
                    UI.menuUI(updateAvailable)

                case "openFolder":
                    startfile(path.abspath("Sábados/"))
                    UI.UIInteraction(False, updateAvailable)

                case "getConfig":
                    UI.configUI(updateAvailable)

                case "getUpdate":
                    VersionManager.getUpdate()

                case "exit":
                    system("cls" if name == "nt" else "clear")
                    exit()

                case _ if returnValue in SETTING_TYPES:
                    Config.getNewConfigValue(returnValue)
                    UI.configUI(updateAvailable)

                case "swapBool":
                    Config.swapBool()
                    UI.configUI(updateAvailable)

                case "returnMenu":
                    UI.menuUI(updateAvailable)
