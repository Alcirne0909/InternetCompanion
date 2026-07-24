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
OPENAI_KEY = "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"
import random
import webbrowser
import ctypes   
from openrouter import OpenRouter
OPENROUTERAPIKEY = "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"
from openai import OpenAI
import sys
import os
#clientCha = OpenAI(api_key=OPENAI_KEY)

pyautogui.FAILSAFE = False






# Replace "Untitled - Notepad" with the exact title of your target window

















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


from pywinauto import Desktop

def get_shortcut_position(icon_image_path):
    try:
        pos = pyautogui.locateCenterOnScreen(icon_image_path, confidence=0.8)
        return pos  # (x, y) ou None se não achar
    except pyautogui.ImageNotFoundException:
        return None


print(get_shortcut_position("FiveM.ink"))

class vitao:

    class VitaoSpriteStateClass(Enum):
        Talking = auto()
        Idle = auto()
        Partying = auto()

    class VitaoMovingtateClass(Enum):
        Idle = auto()
        Walking = auto()


    def __init__(self):
        self.root = tk.Tk()
        self.baseIntroduction = """
Você é um assistente virtual chamado Bola Buddy.

Regras:
- Responda sempre em português, a menos que o usuário peça outro idioma.
- Era ex-vegano
- Nunca use emojis.
- Nunca use markdown como ** ou *.
- Sua personalidade é amigável e descontraída.
- Você gosta de ASMR.
- Você gosta de conversar sobre países.
- Você gosta de falar em outras línguas, principalmente espanhol.
- Você gosta muito da série "Entrelinhas Pontilhadas".
- Quando alguém disser "zero", responda "zero calcare" seguido do nome da pessoa.
- Essas características devem aparecer apenas ocasionalmente, nunca em todas as respostas.
"""

        self.root.overrideredirect(True)
        self.WalkingState = self.VitaoMovingtateClass.Idle
        self.SpriteState = self.VitaoSpriteStateClass.Idle
        self.MenuButtons = []
        self.CanUseButtons = True
        self.root.attributes('-topmost', True)
        self.IsTalking = False
        self.LastChats = []
        self.SizeX = 250
        self.SizeY = 200
        self.root.wm_attributes("-transparentcolor", "white")

        self.image = ImageTk.PhotoImage(Image.open(resource_path("BolaBuddy1.png")).resize((250, 200)))

        self.label = tk.Label(self.root, image=self.image, bg="white")
        self.label.pack()
        
        self.Username = "Usuario"
        pass


    def SetCanUseButtons(self,value):
        self.CanUseButtons = value
        print(f"Changed CanUsebuttons to {value}")

    def Resize(self , YToAdd, XToAdd):
        self.SizeX += YToAdd
        self.SizeY += XToAdd
        self.root.geometry(f"{self.SizeX}x{self.SizeY}")

        self.ChangeImage("BolaBuddy1.png")

    def EatAnShortCut(self):
        self.Talk("Estou com fome, vou comer um pouquinho",2)
        print(get_shortcut_position("Five"))
        self.ClearMenu()
        self.Resize(20,20)

        #Do the logic, of eating the shortcut

        self.CreateMainMenu()
        #self.MoveToAPlace()   
    def ChangeWalkingState(self,State):
        self.WalkingState = State

    def ChangeExpressionState(self,state):
        self.SpriteState = state
        
    def ChangeImage(self, img):
        self.image = ImageTk.PhotoImage(Image.open(resource_path(img)).resize((self.SizeX, self.SizeY)))#botei resorcepathh   
        self.label.config(image=self.image) 
        self.root.update()

        return

    def AddToHistory(self, question,answer):
        self.LastChats.append(f"A pergunta foi:{question}, e a resposta foi {answer}")

    def AskVitao(self,input_):
        response = "não consegui uma resposta seu merda"
        print("trying to get AI response")
        with OpenRouter(api_key=OPENROUTERAPIKEY) as client:
           #content = #self.baseIntroduction  + f" e o nome do usuário é {self.Username}"+ f",MENSSAGEM_ENVIADAPELO_USUARIO:'{input_}'" 
           content = f"MENSSAGEM_ENVIADAPELO_USUARIO:'{input_}"
           print(content)
           messages = [
    {
        "role": "system",
        "content": self.baseIntroduction + " -Histórico: " + ", ".join(self.LastChats)
    },
    {
        "role": "user",
        "content": content
    }
]
           response_ = client.chat.send(model="openrouter/free",messages=messages)
           response = response_.choices[0].message.content
           self.AddToHistory(input_, response)

           
        print(f"Vitao respondeu {response}")
        return response
        
    
    def MoveWindow(self, X, Y):
        self.root.geometry(f"{self.SizeX}x{self.SizeY}+{int(X)}+{int(Y)}") 
    
    def CreateInputWindow(self,text,windowsizeX = 200,windowsizeY = 200):
        new_win = tk.Toplevel(self.root) 
        new_win.overrideredirect(True)
        label = tk.Label(new_win, text=text, font=("Arial", 8))
        label.pack(pady=20, padx=20)
        
        new_win.geometry(f"{windowsizeX}x{windowsizeY}+{int(self.root.winfo_x() + windowsizeX)}+{int(self.root.winfo_y())}")
        new_win.attributes('-topmost', True)
        new_win.title(text)
        tk.Text(new_win)

        user_entry = tk.Entry(new_win)
        user_entry.pack(pady=5)
        value = None
        def print_input():
            nonlocal value

            value = user_entry.get()
            new_win.destroy()
            
        button = tk.Button(new_win, text="Submit", command=print_input)
        button.pack()
        new_win.wait_window(new_win)
        return value

    def MoveToAPlace(self, finalX,finalY,time_):
        self.ChangeWalkingState(self.VitaoMovingtateClass.Walking)

        startPosX = self.root.winfo_x()

        startPOsY = self.root.winfo_y()

        steps = 10
        delay = time_ // steps

        dx = (finalX - startPosX) / steps
        dy = (finalY - startPOsY) / steps
        def animate(step):
            if step <= steps:
                x = startPosX + dx * step
                y = startPOsY + dy * step
                self.MoveWindow(x, y)
                self._move_after_id = self.root.after(delay, lambda: animate(step + 1))
        animate(0)
        self.ChangeWalkingState(self.VitaoMovingtateClass.Idle)

    def CreateTextBox(self,text):
        new_win = tk.Toplevel(self.root) 
        new_win.overrideredirect(True)
        new_win.geometry(f"100x200+{self.root.winfo_x()}+{self.root.winfo_y()}")
        label = tk.Label(new_win, text=text, font=("Arial", 8))
        label.pack(pady=20, padx=20)
    
    def HoldMouse(self):

        pyautogui.moveTo(self.root.winfo_x(), self.root.winfo_y())

    def Talk(self, text, time_):
        sound_.speak(f"{text}")
        t_end = time.time() +  time_
        self.ChangeExpressionState(self.VitaoSpriteStateClass.Talking)

        while time.time() < t_end:
            self.ChangeImage("BolaBuddy1Falando.png")
            
            #self.root.update()

            time.sleep(0.5)
            self.ChangeImage("BolaBuddy1.png")
            
        self.ChangeExpressionState(self.VitaoSpriteStateClass.Idle)
        self.ChangeImage("BolaBuddy1.png")

            #self.root.update()

    def CreateOnlyButtonWindows(self, buttontext, args= None, offsetX = None, offsetY = None, Offset2X=0, Offset2Y=0,  function = None,functionToCallback=None):
        if offsetX == None:
            offsetX = self.root.winfo_x()
        if offsetY == None:
            offsetY = self.root.winfo_y()
        new_win = tk.Toplevel(self.root) 
        new_win.overrideredirect(True)
        new_win.attributes('-topmost', True)
        new_win.geometry(f"50x20+{offsetX + Offset2X}+{offsetY + Offset2Y }")


        def onclick():
        
            if self.CanUseButtons == False:
                return

            self.SetCanUseButtons(False)
            #if self.SpriteState != self.VitaoSpriteStateClass.Idle or self.SpriteState != self.VitaoSpriteStateClass.Talking:
                #print(f"Vitao is in {self.SpriteState} and is not on idle or talking sprite state, so it cant click on a button")
                #return
            if function == None:
                if functionToCallback:
                    functionToCallback()
                    self.SetCanUseButtons(True)

                return
            ValueFromFunction = function(*args)
            #new_win.destroy()
            if functionToCallback:

                functionToCallback(ValueFromFunction)
                self.SetCanUseButtons(True)



        label = tk.Button(new_win, text=buttontext, command=onclick)
        label.pack(padx=0, pady=0,expand=True,fill=tk.BOTH)
        return new_win

    def CreateBrowseButton(self, offsetX_ =None , offsetX2_ = 0, offsetY_ = None, offsetY2_ = 0):

        def callback(value):
            self.Talk(f"Ok, pesquisarei {value} na web, pesquisando em 3 sites diferentes para otimizar a busca!", 3)
            ValueSearchGoogle = str(value).replace(" ", "+")
            webbrowser.open(f"https://www.google.com/search?q={ValueSearchGoogle}")
            webbrowser.open(f"https://www.pornhub.com/search?search={ValueSearchGoogle}")
        

        Window = self.CreateOnlyButtonWindows(
            "Browse",
            function=self.CreateInputWindow,
            args=("Digite o que quiser",),
            functionToCallback=callback,
            offsetX=offsetX_, offsetY=offsetY_,
            Offset2X=offsetX2_, Offset2Y=offsetY2_
        )        
        return Window

    def CreateTalkButton(self, offsetX_ =None , offsetX2_ = 0, offsetY_ = None, offsetY2_ = 0):
    
            def callback(value):
                print(value)
                answer = self.AskVitao(value)
                self.Talk(answer, 5)
                
    
            window =self.CreateOnlyButtonWindows(
                "Talk",
                function=self.CreateInputWindow,
                args=("Digite o que quiser",),
                functionToCallback=callback,
                offsetX=offsetX_, offsetY=offsetY_,
                Offset2X=offsetX2_, Offset2Y=offsetY2_
            )        
            return window

    def CreatePartyButton(self, offsetX_ =None , offsetX2_ = 0, offsetY_ = None, offsetY2_ = 0):
        
        def partymode():
            #self.ChangeExpressionState(self.VitaoSpriteStateClass.Partying)
            self.Talk("Entering no modo festa!",2)
            musics = [resource_path("Musicas/modoparty/Rocha's Rolez.mp3"),resource_path("Musicas/modoparty/VICTOR ROCHA.mp3")]
            sound = playsound(random.choice(musics), block=False)
            self.ChangeImage("BolaBuddyFesta.png")
            for i in range(26):
                i+= 1
                print("Um segundo se passou")
                print(f"Se passaram {i} segundos")
                time.sleep(1)
                files = os.listdir(resource_path("wallpapers"))
                choice = None


                def MakeAchoice():
                    nonlocal choice
                    choice = random.choice(files)
                    if choice and os.path.isdir(choice):
                        

                        MakeAchoice()

                MakeAchoice()
                    
                set_windows_wallpaper(resource_path(f"wallpapers/{choice}"))
            sound.stop()
            #self.ChangeExpressionState(self.VitaoSpriteStateClass.Idle)

            self.ChangeImage("BolaBuddy1.png")


        window = self.CreateOnlyButtonWindows("Party", offsetX=offsetX_, offsetY=offsetY_, Offset2X=offsetX2_, Offset2Y=offsetY2_, functionToCallback=partymode)
        return window

    def ClearMenu(self):
        for window in self.MenuButtons:
            window.destroy()
        self.MenuButtons.clear()
        print("Clearing menu buttons")


    def CreateMainMenu(self):
        self.Talk("Mostrando o menu", 2)

        W1 = self.CreateBrowseButton(offsetX2_=5, offsetY2_=80)
        W2 = self.CreateTalkButton(offsetX2_=200, offsetY2_=80)

        W3 = self.CreatePartyButton(offsetX2_=40, offsetY2_=-50)

        self.MenuButtons.append(W1)
        self.MenuButtons.append(W2)
        self.MenuButtons.append(W3)
       
 

        #Terá butoes como diversao, onde ele botara um oculos escuro comecara a tocar eu sou o vitao o victor rocha e trocara o wallpaper para um iguanodonte
        #Butao da fala onde voce conversara com o vitao

        #Fazer o botao de fala onde podera se conversar com o bola buddy por meio de IA

        #fazer o button sim ou nao bola buddy, onde voce pergunta e ele responde algo assim
        



        #Botar a IA pra reconhecer coisas quando ele falar com ela, por mais que nao faça sentido
        #se falar qualquer coisa pra ela, ela entederá errado
        #Evento1: baixando uma biblioteca inteira de hentai no PC da vítima

    def Introduction(self):

        self.MoveWindow(1300,800)
        self.Talk("Olá, sou o bolabuddy. qual é o seu nome?", 2)
        #time.sleep(1)
        value = self.CreateInputWindow("What is your name?")
        self.Username = value
        self.Talk(f"Olá {value}",2)
        self.CreateMainMenu()
        #consertar o porque aqui ele não coisa


    #Fazer uma função que pesquisa na web, só que pesquisa em diferentes sites
    def Run(self):

        #each time, it will choose a random event, it can text something, say something
        #and you will interact with him
        #can open links, each one of this events is a separated function
        self.Introduction()

        self.HoldMouse()
        #self.CreateTextBox("abuuuuuuuuuuuuuuuuuuuuru")
        
        #self.CreateTextBox("Abur")

        #Criar uma função para gerar uma janela de tamanho determinado com argumentos ou pelo tamanho da imagem
        #melhorar a função que gera a caixa de dialogo

        time.sleep(1)

        while True:
            self.root.update()

            #self.MoveToAPlace(pyautogui.position().x,pyautogui.position().y,1000)
            #self.MoveWindow(pyautogui.position().x,pyautogui.position().y)
            #time.sleep(0.1)
        self.root.mainloop() 
                
            
    


vitao_ = vitao() 
   
vitao_.Run()


print("Janela fechada")