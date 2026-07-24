
import tkinter as tk
import time
import pyautogui # type: ignore
from PIL import Image, ImageTk
import pyttsx3
import queue

import threading
from enum import Enum, auto
from playsound3 import playsound
import random
import webbrowser
import ctypes   
from openrouter import OpenRouter
from dotenv import load_dotenv


import sys
import os






load_dotenv()

OPENROUTERAPIKEY = os.getenv("KEY")


def CheckifFolderHasBeenModified(folderpath, callback):
    files_before = set(os.listdir(folderpath))
    while True:

        files_now = set(os.listdir(folderpath))
        new_files = files_now - files_before
        
        if new_files:
            for f in new_files:
                print(f"Novo arquivo detectado: {f}")
                callback(f, folderpath)
                files_before = files_now
        time.sleep(1)
        



def create_folder_with_icon(folder_path, icon_path):
    """
    Cria uma pasta e define um ícone customizado para ela.
    icon_path deve ser o caminho para um arquivo .ico
    """
    # 1. Cria a pasta
    os.makedirs(folder_path, exist_ok=True)

    # 2. Cria o desktop.ini dentro dela
    ini_path = os.path.join(folder_path, "desktop.ini")
    icon_abs_path = os.path.abspath(icon_path)

    with open(ini_path, "w") as f:
        f.write("[.ShellClassInfo]\n")
        f.write(f"IconResource={icon_abs_path},0\n")

    # 3. Marca o desktop.ini como oculto + sistema (obrigatório pro Windows respeitar)
    FILE_ATTRIBUTE_HIDDEN = 0x02
    FILE_ATTRIBUTE_SYSTEM = 0x04
    ctypes.windll.kernel32.SetFileAttributesW(
        ini_path, FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM
    )

    # 4. Marca a própria pasta como "read-only" (é o que sinaliza pro Explorer
    # que essa pasta tem configurações customizadas via desktop.ini)
    FILE_ATTRIBUTE_READONLY = 0x01
    ctypes.windll.kernel32.SetFileAttributesW(folder_path, FILE_ATTRIBUTE_READONLY)

    # 5. Força o Explorer a atualizar o ícone imediatamente
    SHCNE_ASSOCCHANGED = 0x08000000
    SHCNF_IDLIST = 0x0000
    ctypes.windll.shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)

def resource_path(relative_path):
    """Retorna o caminho absoluto do recurso, funcionando tanto em dev quanto empacotado."""
    try:
        base_path = sys._MEIPASS  # pasta temporária criada pelo PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def set_windows_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDCHANGE = 0x02

    abs_path = os.path.abspath(image_path)

    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"Imagem não encontrada: {abs_path}")

    # Converte para BMP se necessário (formato mais confiável para essa API)
    if not abs_path.lower().endswith('.bmp'):
        bmp_path = os.path.join(
            os.path.dirname(abs_path),
            os.path.splitext(os.path.basename(abs_path))[0] + '_wallpaper.bmp'
        )
        Image.open(abs_path).convert('RGB').save(bmp_path, 'BMP')
        abs_path = bmp_path

    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        abs_path,
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )

    if not result:
        raise ctypes.WinError(ctypes.get_last_error())

    return abs_path

class sound:
    def __init__(self):
        self.queque_ = queue.Queue()
        self.engine = None
        self._worker = threading.Thread(target=self.run, daemon=True)
        self._worker.start()
        # Initialize the engine
        
    def run(self):
        self.engine = pyttsx3.init()

        # Set properties (optional)
        voices = self.engine.getProperty("voices")

        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 1.0) # Volume 0.0 to 1.0
        for voice in voices:
            if 'pt' in voice.languages or 'brazil' in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break
        while True:
            text = self.queque_.get()

            if text is None:
                break
            self.say(text)

    
    def say(self,text):
        self.engine.say(text)
        self.engine.startLoop(False)
        while self.engine.isBusy():
             self.engine.iterate()
        self.engine.endLoop()
        
    def speak(self, text):
        
        self.queque_.put(text)

sound_ = sound()




















