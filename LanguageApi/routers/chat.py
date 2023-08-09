from services.chat_service import Chat
from services.runpod_service import RunpodAPI

from schemas.chat_schemas import ChatRequest, ChatResponse

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/chat")


@router.post("/{chat_id}")
async def chat_text_to_text(chat_id: str, request: ChatRequest):
    chat = await Chat.load(chat_id)
    return ChatResponse(response=await chat.send_message(request.prompt))


@router.post("/{chat_id}")
async def chat_audio_to_text(chat_id: str, file: UploadFile):
    transcription = RunpodAPI().transcode(await file.read())
    chat = await Chat.load(chat_id)
    return ChatResponse(response=await chat.send_message(transcription))


@router.get("/{chat_id}")
async def get_usage(chat_id: str):
    chat = await Chat.load(chat_id)
    print(chat.token_usage())
    return JSONResponse(content={"tokens_used": chat.token_usage()})


@router.put("/{chat_id}")
async def create_with_custom_persona(chat_id: str, request: ChatRequest):
    await Chat.create_with_custom_persona(chat_id, request.prompt)


@router.delete("/{chat_id}")
async def clear(chat_id: str):
    chat = Chat(chat_id)
    await chat.clear()
