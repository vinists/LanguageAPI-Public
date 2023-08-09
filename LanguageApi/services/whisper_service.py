from io import IOBase

import requests
from helper import utils


class Whisper:
    def __init__(self):
        self.url = "http://192.168.1.18:9001/asr"
        self.headers = {
            'accept': 'application/json'
        }

    def transcribe_audio(self, audio: IOBase):
        # Preparing audio file data
        audio_file = ('audio_file', (utils.get_epoch_filename("ogg"), audio, 'audio/ogg'))

        response = requests.post(
            self.url,
            headers=self.headers,
            params={
                'method': 'openai-whisper',
                'task': 'transcribe',
                'encode': 'true',
                'output': 'json',
            },
            files=[audio_file]
        )

        result = response.json()

        return {"text": result["text"], "language": result["language"]}
