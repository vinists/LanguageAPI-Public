import requests
import json
from .s3_service import S3


from config import Settings, get_settings
settings: Settings = get_settings()


class RunpodAPI:
    def __init__(self):
        self.url = "https://api.runpod.ai/v2/faster-whisper/runsync"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": settings.runpod_apikey
        }

    def whisper_transcode(self, audio_url, model="base", transcription="plain text", translate=False,
                          temperature=0, best_of=5, beam_size=5, suppress_tokens="-1",
                          condition_on_previous_text=False, temperature_increment_on_fallback=0.2,
                          compression_ratio_threshold=2.4, logprob_threshold=-1, no_speech_threshold=0.6):
        payload = {
            "input": {
                "audio": audio_url,
                "model": model,
                "transcription": transcription,
                "translate": translate,
                "temperature": temperature,
                "best_of": best_of,
                "beam_size": beam_size,
                "suppress_tokens": suppress_tokens,
                "condition_on_previous_text": condition_on_previous_text,
                "temperature_increment_on_fallback": temperature_increment_on_fallback,
                "compression_ratio_threshold": compression_ratio_threshold,
                "logprob_threshold": logprob_threshold,
                "no_speech_threshold": no_speech_threshold
            }
        }

        response = requests.post(self.url, json=payload, headers=self.headers)
        return " ".join([x["text"] for x in response.json()["output"]["segments"]])

    def transcode(self, audio_file: bytes):
        return self.whisper_transcode(S3().upload_file(audio_file))
