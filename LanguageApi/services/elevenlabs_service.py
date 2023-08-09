import requests

from config import Settings, get_settings
settings: Settings = get_settings()


class ElevenLabsAPI:
    def __init__(self):
        self.api_key = settings.elevenlabs_apikey
        self.base_url = "https://api.elevenlabs.io/v1/text-to-speech"
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

    def generate_speech(self, text: str, voice_id: str = "EXAVITQu4vr4xnSDxMaL", model_id: str = "eleven_multilingual_v1"):
        url = f"{self.base_url}/{voice_id}/stream"
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        response = requests.post(url, json=data, headers=self.headers, stream=True)
        if response.status_code == 200:
            return response

        raise ConnectionError
