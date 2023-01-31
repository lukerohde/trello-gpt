import openai
class ChatGPT():
    def __init__(self, model, key):
        openai.api_key = key
        self.model = model
        self.tokens = 0
        self.temperature = 0.8
        self.max_tokens = 256
        self.frequency_penalty = 1
    
    def answer(self, history):
        response = openai.Completion.create(model=self.model, prompt=history, temperature=self.temperature, max_tokens=self.max_tokens, frequency_penalty = self.frequency_penalty)
        self.tokens = response['usage']['total_tokens']
        answer = response["choices"][0]["text"]
        
        return answer
    
