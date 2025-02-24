from os import system
from queue import Queue
from pynput.keyboard import Listener
from versionmanager import VersionManager
from config import Config
from win32gui import GetWindowText, GetForegroundWindow
from main import main
import msvcrt


keyPressReturnValue = Queue()


class UI:
    @staticmethod
    def menuUI(updateAvailable: bool) -> None:
        system("clear||cls")
        print(
            "\n███╗   ███╗███╗   ███╗ █████╗  ██████╗██████╗\n████╗ ████║████╗ ████║██╔══██╗██╔════╝██╔══██╗\n██╔████╔██║██╔████╔██║███████║██║     ██████╔╝\n██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║     ██╔═══╝\n██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║╚██████╗██║\n╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝\n\n"
        )

        if updateAvailable:
            print(
                "[1] Run\n[2] Settings\n[3] \033[31mUpdate Available!\033[0m\n[4] Exit"
            )
            UI.UIInteraction(False, updateAvailable)
            return

        print("[1] Run\n[2] Settings\n[3] No Update Available\n[4] Exit")
        UI.UIInteraction(False, updateAvailable)

    @staticmethod
    def on_press(key, config: bool, updateAvailable: bool) -> None:
        if GetWindowText(GetForegroundWindow()) in ["MMACP", "Windows PowerShell"]:
            try:
                if not config:
                    # Check Settings
                    if key.char == "2":
                        keyPressReturnValue.put("getConfig")
                        return False

                    # Update if available
                    if updateAvailable:
                        if key.char == "3":
                            keyPressReturnValue.put("getUpdate")
                            return False
                else:
                    if key.char == "2":
                        keyPressReturnValue.put("swapBool")
                        return False

            except AttributeError:
                pass

    @staticmethod
    def on_release(key, config: bool) -> None | bool:
        while msvcrt.kbhit():
            msvcrt.getch()
        if GetWindowText(GetForegroundWindow()) in ["MMACP", "Windows PowerShell"]:
            try:
                if not config:
                    if key.char == "1":
                        keyPressReturnValue.put("runMain")
                        return False

                    if key.char == "4":
                        keyPressReturnValue.put("exit")
                        return False
                else:
                    if key.char == "1":
                        keyPressReturnValue.put("spreadSheetIDChange")
                        return False

                    if key.char == ("3"):
                        keyPressReturnValue.put("returnMenu")
                        return False

            except AttributeError:
                pass

    @staticmethod
    def UIInteraction(config: bool, updateAvailable: bool) -> None:
        with Listener(
            on_press=lambda event: UI.on_press(event, config, updateAvailable),
            on_release=lambda event: UI.on_release(event, config),
        ) as listener:
            listener.join()

    @staticmethod
    def configUI(updateAvailable: bool) -> None:
        system("clear||cls")
        print(
            "\n███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗\n██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝\n███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗\n╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║\n███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║\n╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝\n\n"
        )
        print(f"[1] Spreadsheet ID: {Config.getkeys('sheetid')}")
        print(f"[2] YouTube Usage: {Config.getkeys('youtube')}")
        print("[3] Return")
        UI.UIInteraction(True, updateAvailable)

    def mainUI(updateAvailable: bool) -> None:
        UI.menuUI(updateAvailable)
        while True:
            returnValue: str = keyPressReturnValue.get()
            match returnValue:
                case "runMain":
                    main()
                    UI.menuUI(updateAvailable)

                case "getConfig":
                    UI.configUI(updateAvailable)

                case "getUpdate":
                    VersionManager.getUpdate()

                case "exit":
                    return

                case "spreadSheetIDChange":
                    Config.getSpreadsheetID()
                    UI.configUI(updateAvailable)

                case "swapBool":
                    Config.swapBool()
                    UI.configUI(updateAvailable)

                case "returnMenu":
                    UI.menuUI(updateAvailable)
