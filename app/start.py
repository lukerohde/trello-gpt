import os
import json

from texttospeech import TextToSpeech
from chatgpt import ChatGPT
from config import Config
from application import Application
from trello import Trello 

config = Config(
    botname = os.getenv("BOT_NAME"),
    username = os.getenv("USER_NAME"),
    speech_prefix = os.getenv("SPEECH_PREFIX"),
    primer_file = os.getenv("PRIMER_FILE"),
    editor = os.getenv("EDITOR") or "nano", 
    bot = ChatGPT(
        os.getenv("OPENAI_API_KEY"), 
        os.getenv("GPT_MODEL") or "text-davinci-003", 
        os.getenv("GPT_TEMP") or "0.8", 
        os.getenv("GPT_TOKENS") or 256),
    voice=TextToSpeech(os.getenv("AZURE_ENDPOINT"), os.getenv("AZURE_API_KEY"), os.getenv("AZURE_VOICE")),
    trello=Trello(os.getenv("TRELLO_ENDPOINT"), os.getenv("TRELLO_API_KEY"), os.getenv("TRELLO_TOKEN"))
)

app = Application(config)
app.go()


    

            


    
