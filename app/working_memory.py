# TODO
# Keep a persistent histor of each Q&A as a list of posts
# Pass Response + Question into memory for recall
# Include timestamp in each - I don't think iso is properly tokanizeable
# Consider regex-ing out user and bot name - so they can be subbed
# Consider a means to set an objective?
# Load converstation history up to buffer
# Consider having 'no that's wrong, please forget memories' that if triggered cause memory items to be deleted
# Success criteria is an adventure that can pickup, where it left off and remember the full context, including inventory

import os
import json
import datetime

class WorkingMemory:
    def __init__(self) -> None:
        self.config = None
        self.history = []
        self.memory_count = 3 # TBD make config

    def set_config(self, config):
        self.config = config

        self.history_path = os.path.join(".", "memory", self.config.botname )
        if not os.path.exists(self.history_path):
            os.makedirs(self.history_path)

        self.history_path = os.path.join(self.history_path, 'history.txt')
        
        self._load_history()


    def add_dialog(self, agent, timestamp, prompt):
        dialog = {
            'agent': agent, 
            'timestamp': timestamp.strftime('%A %d %B %Y %I:%M%p'), 
            'prompt': prompt
        }
        
        self.history.append(dialog)
        self._save_history()
        if agent == self.config.botname:
            self._update_memory(self._memory_episode())

        return self._format_dialog(dialog) # this isn't needed

    def retrieve(self):
        
        # load our bot primer fresh everytime
        result = "## Intro\n"
        result += self._primer() 
        
        # load memories
        memories = self._retrieve_memories()
        if len(memories):
            result += f"\n\n## {self.config.botname} keep this in mind when answering. \n" 
            result += self._format_memories(memories)

        #keep as much coversation history as possible in memory
        select_history = []
        for item in reversed(self.history):
            dialog = self._format_dialog(item)
            if self._overloaded(result + "\n".join(select_history)): break
            select_history.append(dialog)

        #result += "\n\n## Chat History\n" 
        result += "\n".join(reversed(select_history))

        # write the working memory to disk for inspection
        with open(os.path.join("tmp","working_memory.txt"), "w") as f:
            f.write(result)

        return result

    def forget_history(self):
        self.history = []
        self._save_history()

    
    def _overloaded(self, working_memory):
        tokens = len(working_memory) / self.config.token_length + self.config.response_tokens
        return True if tokens > self.config.max_tokens else False

    def _retrieve_memories(self):
        result = self._memory_episode()
        result = self.config.long_term_memory.recall(result, self.memory_count)
        return result

    def _update_memory(self, episode):
        result = self.config.long_term_memory.memorize(episode)
        return result # not necessary
    
    def _memory_episode(self):
        result = [ self._format_dialog(item) for item in self.history[-2:] ]
        result = f"\n".join(result)
        return result

    def _load_history(self):
        self.history = []
        if os.path.exists(self.history_path):
            with open(self.history_path, 'r') as f: 
                result = f.read()
                result = json.loads(result)
                self.history = result


    def _save_history(self):
        # This is a bit crap, because it rewrites the whole history on every prompt
        with open(self.history_path,'w') as f: 
            json.dump(self.history,f)

    def _primer(self):
        result = ""
        with open(self.config.primer_file, "r") as f:
            result = f.read()
            result = result.format(botname=self.config.botname,username=self.config.username)
        return result

    def _format_memories(self, memories):
        # put a pipe in front of everything
        fm = [ self._format_memory(memory) for memory in memories ]
        result = f"\n".join(fm)
        return result

    # def _format_memory(self, memory):
    #     result = f"### {memory['timestamp']}\n"
    #     result += '>' + memory['string'].replace('\n', '\n>')
    #     return result

    def _format_memory(self, memory):
        result = f"### {self.config.botname} remembers {memory['timestamp']}\n"
        result += '' + memory['string'].replace('\n', '\n')
        result += "---\n"
        return result


    def _format_dialog(self, item):
        #result = item.get('timestamp', '') + "\n"
        result = item.get('agent', '') + ": "
        result += item.get('prompt', '')
        result += "\n\n"
        return result

    # def prompt(self):
    #     pass



    # def please_respond(self):
    #     # I'm not sure if we want this a separate call from prompt
    #     # I'm imagining the UI waiting till the user stops typing before responding
    #     # I'm also imagining threaded background processing of prompts
    #     # where the work starts while the user is typing
    #     # and maybe, the bot can respond multiple times as background threads return (erk)
    #     pass

    # def _context_summary(self):
    #     pass

    # def _memories(self):
    #     # the act of memorizing, adds a memory, becareful what we call
    #     # I think it should be context and prompt
    #     # prompt stores user inputs, containing key
    #     pass

    # def _working_memory(self, input):
    #     # need token/length management
    #     # the api calls here are sucky
    #     # context_summary is one way of compressing tokens
    #     # but context_summary might be important for memories too
    #     result = self.primer()
    #     context = self._context_summary() # api call to summarize recent convo
    #     result += self.memories(context) # api call for embedding
    #     result += context()
    #     result += input

    #     return result





    #             def compose_prompt(self, primer, user_prompt, memories, history):
    #     result = primer
    #     formatted_memories = [ self._format_memory(item) for item in memories ]
    #     formatted_memories = f"\n".join(formatted_memories)
    #     result += "\n" + formatted_memories 
    #     result += history
    #     result += self._history_update(user_prompt, "")

    #     with open("gpt_prompt.txt", "w") as f:
    #         f.write(result)

    #     return result

    #     memories = self.config.long_term_memory.recall(prompt,3)


    # def _history_update(self, user_prompt, response):
    #     result = f"\n\n{self.config.username}: " + user_prompt + "\n"
    #     result += f"\n\n{self.config.botname}: " + response + "\n"
    #     return result



