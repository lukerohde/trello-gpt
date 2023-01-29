import os
import json

from texttospeech import TextToSpeech
from chatgpt import ChatGPT
from config import Config
from application import Application

config = Config(
    botname = os.getenv("BOT_NAME"),
    username = os.getenv("USER_NAME"),
    speech_prefix = os.getenv("SPEECH_PREFIX"),
    primer_file = os.getenv("PRIMER_FILE"),
    bot = ChatGPT("text-davinci-003", os.getenv("OPENAI_API_KEY")),
    voice=TextToSpeech(os.getenv("AZURE_ENDPOINT"), os.getenv("AZURE_API_KEY"), os.getenv("AZURE_VOICE"))
)

app = Application(config)
app.go()


    

            


    
