import re
import os
import subprocess 
import datetime

class Application:
    def __init__(self, config):
        self.config = config
        
    def go(self):
        while True:
            # Prompt user for input 
            print(self.config.working_memory.retrieve())
            prompt = input(f"\n{self.config.username}('q' to quit, 'r' to replay, 's' to stop, 'f' to forget): ")
            
            if prompt == '':
                prompt = self._prompt_from_editor() 
                
            if prompt.lower() == 'q':
                break
            elif prompt.lower() == 'r':
                self.config.voice.repeat()
            elif prompt.lower() == 's':
                self.config.voice.stop()
            elif prompt.lower() == 'f':
                self.history = self.config.working_memory.forget_history();
            elif prompt[0:3] == "tb ":
                self.history += self.config.trello.get_board(prompt[3:])
            elif prompt[0:2] == "l ":
                self.history += self._load_file(prompt[2:])
            else: 

                self.config.working_memory.add_dialog(
                    self.config.username,
                    datetime.datetime.now(),
                    prompt
                )
                
                bot_memory = self.config.working_memory.retrieve()
                bot_memory += f"\n\n{self.config.botname}: "
                
                answer = self.config.bot.answer(bot_memory)

                self.config.working_memory.add_dialog(
                    self.config.botname,
                    datetime.datetime.now(),
                    answer
                )
                
                if self.config.speech_on:
                    text = self._find_something_to_say(answer)
                
                    if text != "": 
                        self.config.voice.speak_in_background(text)
            
                
        
    def _find_something_to_say(self, text): 
        # Function to speak text in the background 
        if self.config.speech_prefix != "":
            result = re.findall(rf"^{self.config.speech_prefix}:.*", text, re.MULTILINE)
            result = '\n'.join(result)
            result = re.sub(rf"^{self.config.speech_prefix}:", "", result, flags=re.MULTILINE)
        else:
            result = text
            
        result = re.sub(rf"{self.config.botname}:", "", result, flags=re.MULTILINE)  

        return result
    
    def _load_file(self, filename):
        with open(filename, "r") as f:
            history += f"### START OF {filename} ###"
            history += f.read()
            history += f"### END OF {filename} ###"
            
    def _prompt_from_editor(self):
        result = ""
        with open(os.path.join('tmp','temp_prompt.txt'), 'w') as f:  
            f.write('')
        subprocess.call([self.config.editor, os.path.join('tmp','temp_prompt.txt')])
        with open(os.path.join('tmp','temp_prompt.txt'), 'r') as f:  
            result = f.read() 
        return result
            

    