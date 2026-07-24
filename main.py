import tkinter as tk
import time
import pyautogui # type: ignore
from PIL import Image, ImageTk
import pyttsx3
import queue

import threading
from functools import partial
from enum import Enum, auto
from playsound3 import playsound
import random
import webbrowser
import ctypes   
from openrouter import OpenRouter
from dotenv import load_dotenv



import sys
import os

from libs.Vitao import vitao


load_dotenv()

OPENROUTERAPIKEY = os.getenv("KEY")
pyautogui.FAILSAFE = False




# Replace "Untitled - Notepad" with the exact title of your target window





vitao_ = vitao() 
   
vitao_.Run()


print("Janela fechada")