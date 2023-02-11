import threading 
import requests
import simpleaudio as sa

class TextToSpeech():

    def __init__(self, endpoint, key, voice):
        self.endpoint = endpoint
        self.key = key
        self.voice = voice
        self.audio = None
        self.lock = threading.Lock()
        self._play_obj = None
        
    def speak_in_background(self, text):
        t = threading.Thread(target=self.speak, args=(text,)) 
        t.start()
        
    def speak(self, text):
        with self.lock: 
            self.audio = self._text_to_speech(text)
        self._play_audio(self.audio) 
    
    def stop(self):
        self._play_obj.stop()    
    
    def repeat(self):
        if self.audio != None:
            self._play_audio(self.audio) 

    def _text_to_speech(self, text):
        # Define the request headers
        headers = {
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "raw-8khz-16bit-mono-pcm",
            "Ocp-Apim-Subscription-Key": f"{self.key}",
        }

        # Define the request body
        body = "<speak version='1.0' xmlns='https://www.w3.org/2001/10/synthesis' xml:lang='en-US'>" \
               f"<voice xml:lang='en-US' xml:gender='Male' name='{self.voice}'>" \
               f"{text}" \
               "</voice>" \
               "</speak>"
              

        # Make the request
        response = requests.post(self.endpoint, headers=headers, data=body.encode('UTF-8'))
        # Return the response audio
        return response.content

    # Function to play the audio
    def _play_audio(self, audio_data):
        wave_obj = sa.WaveObject(audio_data,1,2,8000)
        with self.lock: 
            self._play_obj = wave_obj.play()
        #self._play_obj.wait_done()
        
            

