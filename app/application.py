import re

class Application:
    def __init__(self, config):
        self.config = config
        self.history = self._primer()


    def go(self):
        while True:
            # Prompt user for input
            print(self.history)
            print(f"TOKENS: {self.config.bot.tokens}");

            prompt = input(f"\n{self.config.username}('q' to quit, 'r' to replay, 's' to stop, 'f' to forget): ")

            if prompt.lower() == 'q':
                break
            elif prompt.lower() == 'r':
                self.config.voice.repeat()
            elif prompt.lower() == 's':
                self.config.voice.stop()
            elif prompt.lower() == 'f':
                self.history = self._primer();
            elif prompt[0:3] == "tb ":
                self.history += self.config.trello.get_board(prompt[3:])
            elif prompt[0:2] == "l ":
                self.history += self._load_file(prompt[2:])
            else: 
                self.history += f"\n\n{self.config.username}: " + prompt + "\n"
                answer = self.config.bot.answer(self.history)

                text = self._find_something_to_say(answer)
                
                if text != "": 
                    self.config.voice.speak_in_background(text)

                self.history += answer + "\n\n----"
    
    def _primer(self):
        result = ""
        with open(self.config.primer_file, "r") as f:
            result = f.read()
            result = result.format(botname=self.config.botname,username=self.config.username)
        return result
        
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
            history = f"### START OF {filename} ###"
            history += f.read()
            history += f"### END OF {filename} ###"
        return history

    
