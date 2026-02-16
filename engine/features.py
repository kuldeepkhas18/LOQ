import re
from shlex import quote
import sqlite3
import struct
import subprocess
import time
import webbrowser
import hugchat
from playsound import playsound
import eel
import os

import pvporcupine
import pyaudio
import pyautogui
from engine.config import ASSISTANT_NAME
from engine.command import speak
#play assiastant sound function
import pywhatkit as kit

from engine.helper import extract_yt_term, remove_words
from hugchat.hugchat import ChatBot


con = sqlite3.connect(r"C:\code\LOQ\engine\LOQ.db")
cursor = con.cursor()

@eel.expose
def playAssistantsound():
    music_dir ="C:\\code\\LOQ\\www\\assets\\audio\\loq sound.mp3"
    playsound(music_dir)

playAssistantsound()

def openCommand(query):
    print("open command called with",query)

    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()

    query = re.sub(r'\s+', ' ', query)
    app_name = query.strip()

    if app_name == "youtube":
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        return
    
    if app_name == "canva":
        speak("Opening Canva")
        webbrowser.open("https://www.canva.com")
        return

    if app_name != "":  
        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name = ?', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+ app_name)
                os.startfile(results[0][0])
            else:
                cursor.execute(
                    'SELECT url FROM web_command WHERE LOWER(name) = ?',
                    (app_name.lower(),)
                )
                results = cursor.fetchall()

            if len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE LOWER(name) = ?', (app_name.lower(),))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

 

def PlayYoutube(query):
    search_term = extract_yt_term(query)

    if search_term is None:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        return
    
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term) 


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
        
        #pre trained keywords
        porcupine=pvporcupine.create(keywords=["LOQ","alexa"])
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)

        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            #processing keyword comes from mic
            keyword_index=porcupine.process(keyword)

            #processing keyword comes from mic
            keyword_index=porcupine.process(keyword)

            #checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                #pressing shorcut key with+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyup("win")

    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


#### 8. Create find contacts number Function in features.py
# Whatsapp Message Sending

def findContact(query):

    print("DEBUG: findContact called")

    cursor.execute("PRAGMA database_list;")
    print("DB PATH:", cursor.fetchall())

    cursor.execute("SELECT COUNT(*) FROM contacts;")
    print("TOTAL CONTACTS:", cursor.fetchone())

    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)
    print("FINAL QUERY AFTER REMOVE:", query)

    try:
        query = query.strip().lower()

        if query == "":
            speak("contact name not clear")
            return 0, 0
        
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(TRIM(name)) LIKE ?",
                        ('%' + query + '%',))
        results = cursor.fetchall()

        if len(results) == 0:
            speak('not exist in contacts')
            return 0, 0

        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0



#### 9. Create Whatsapp Function in features.py

def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 12
        LOQ_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 8
        message = ''
        LOQ_message = "calling to "+name

    elif flag == 'video call':
        target_tab = 9
        message = ''
        LOQ_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(6)
   
    if flag != 'video call':
        pyautogui.hotkey('ctrl', 'f')

    time.sleep(1)   

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(LOQ_message)


def chatBot(query):
    try:
        user_input = query.lower()

        chatbot = ChatBot(
            cookie_path="C:\\code\\LOQ\\engine\\cookies.json"
        )

        convo_id = chatbot.new_conversation()
        chatbot.change_conversation(convo_id)

        response = chatbot.chat(user_input)
        print(response)
        speak(response)
        return response

    except Exception as e:
        print("Error:", e)
        return None