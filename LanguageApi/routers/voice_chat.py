import io

from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse, Response, JSONResponse

import services as svc
from internal import redis_client as r

router = APIRouter(prefix="/voicechat")


@router.post("/{chat_id}")
async def chat_audio_to_audio(chat_id: str, file: UploadFile):
    transcription = svc.RunpodAPI().transcode(await file.read())
    chat = await svc.Chat.load(chat_id)
    print(transcription)

    response = await chat.send_message(transcription)
    print(response)
    stream = svc.ElevenLabsAPI().generate_speech(response)
    return StreamingResponse(stream.iter_content(chunk_size=1024), media_type="audio/mpeg")


@router.post("/{chat_id}/{voice_id}")
async def chat_audio_to_audio_v2(chat_id: str, voice_id: str, file: UploadFile):
    transcription = svc.Whisper().transcribe_audio(io.BytesIO(await file.read()))
    chat = await svc.Chat.load(chat_id)
    print(transcription)

    response = await chat.send_message(transcription["text"])
    print(response)
    result = svc.TextToSpeech().generate_speech(response, voice_id)
    return Response(result, media_type="audio/wav")


@router.post("/discord/{chat_id}/{voice_id}")
async def chat_audio_to_audio_discord(chat_id: str, voice_id: str, file: UploadFile):
    pubsub = r.PubSub(chat_id)
    handshake_result = await pubsub.handshake()

    if handshake_result:
        transcription = svc.Whisper().transcribe_audio(io.BytesIO(await file.read()))

        chat = await svc.Chat.load(chat_id)
        print(transcription)

        response = await chat.send_message(transcription["text"])
        print(response)
        result = svc.TextToSpeech().generate_speech(response, voice_id)

        publish_result = await pubsub.publish(result)

        return JSONResponse(content={"IsPublished": publish_result})


@router.get("/voices")
async def get_voices():
    return JSONResponse(content=svc.TextToSpeech.get_voices())


