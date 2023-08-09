import io

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

from services.runpod_service import RunpodAPI
from services.whisper_service import Whisper

router = APIRouter(prefix="/transcode")


@router.post("/runpod")
async def transcode(file: UploadFile):
    return JSONResponse(content={"Text": RunpodAPI().transcode(await file.read())})


@router.post("/whisper")
async def transcode(file: UploadFile):

    file_raw = await file.read()
    transcription = Whisper().transcribe_audio(io.BytesIO(file_raw))

    return JSONResponse(content={"Text": transcription["text"], "Language": transcription["language"]})