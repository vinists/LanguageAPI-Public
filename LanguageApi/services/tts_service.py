from services.s3_service import S3
import requests


class TextToSpeech:
    def __init__(self):
        self.url = "http://192.168.1.18:9192/api/tts"

    def _generate_speech(self, text: str, speaker_id: str = "p312", style_wav: str = "", language_id: str = "") -> bytes:
        params = {
            'text': text,
            'speaker_id': speaker_id,
            'style_wav': style_wav,
            'language_id': language_id
        }

        response = requests.get(self.url, params=params)

        if response.status_code == 200:
            return response.content

        raise ConnectionError

    def generate_speech(self, text: str, speaker_id: str = "p312"):
        return self._generate_speech(text, speaker_id)

    def generate_speech_s3_url(self, text: str):
        audio = self._generate_speech(text)
        return S3().upload_file(audio)

    @staticmethod
    def get_voices():
        return ['p225', 'p226', 'p227', 'p228', 'p229', 'p230', 'p231', 'p232', 'p233', 'p234', 'p236', 'p237', 'p238', 'p239', 'p240', 'p241', 'p243', 'p244', 'p245', 'p246', 'p247', 'p248', 'p249', 'p250', 'p251', 'p252', 'p253', 'p254', 'p255', 'p256', 'p257', 'p258', 'p259', 'p260', 'p261', 'p262', 'p263', 'p264', 'p265', 'p266', 'p267', 'p268', 'p269', 'p270', 'p271', 'p272', 'p273', 'p274', 'p275', 'p276', 'p277', 'p278', 'p279', 'p280', 'p281', 'p282', 'p283', 'p284', 'p285', 'p286', 'p287', 'p288', 'p292', 'p293', 'p294', 'p295', 'p297', 'p298', 'p299', 'p300', 'p301', 'p302', 'p303', 'p304', 'p305', 'p306', 'p307', 'p308', 'p310', 'p311', 'p312', 'p313', 'p314', 'p316', 'p317', 'p318', 'p323', 'p326', 'p329', 'p330', 'p333', 'p334', 'p335', 'p336', 'p339', 'p340', 'p341', 'p343', 'p345', 'p347', 'p351', 'p360', 'p361', 'p362', 'p363', 'p364', 'p374', 'p376']
