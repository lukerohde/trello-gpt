import os
import json
import ipdb
import datetime

from texttospeech import TextToSpeech
from chatgpt import ChatGPT
from config import Config
from application import Application
from trello import Trello 
from long_term_memory import LongTermMemory
from working_memory import WorkingMemory

config = Config(
    botname = os.getenv("BOT_NAME"),
    username = os.getenv("USER_NAME"),
    speech_on = os.getenv("SPEECH_ON"),
    speech_prefix = os.getenv("SPEECH_PREFIX"),
    primer_file = os.getenv("PRIMER_FILE"),
    response_tokens = os.getenv("GPT_RESPONSE_TOKENS") or 256, 
    max_tokens = os.getenv("GPT_MAX_TOKENS") or 4000, 
    token_length = os.getenv("GPT_TOKENS_LENGTH") or 3.5, 
    editor = os.getenv("EDITOR") or "nano", 
    bot = ChatGPT(
        os.getenv("OPENAI_API_KEY"), 
        os.getenv("GPT_MODEL") or "text-davinci-003", 
        os.getenv("GPT_TEMP") or "0.8", 
        os.getenv("GPT_TOKENS") or 256),
    voice=TextToSpeech(os.getenv("AZURE_ENDPOINT"), os.getenv("AZURE_API_KEY"), os.getenv("AZURE_VOICE")),
    trello=Trello(os.getenv("TRELLO_ENDPOINT"), os.getenv("TRELLO_API_KEY"), os.getenv("TRELLO_TOKEN")),
    long_term_memory=LongTermMemory(os.getenv("OPENAI_API_KEY"), os.getenv("BOT_NAME")),
    working_memory=WorkingMemory()
)

config.working_memory.set_config(config) #hmmm....

app = Application(config)
app.go()

