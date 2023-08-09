from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    aws_region: str = Field(..., env="AWS_DEFAULT_REGION")
    s3_bucket: str = Field(..., env="s3_bucket")

    runpod_apikey: str = Field(..., env="runpod_apikey")
    elevenlabs_apikey: str = Field(..., env="elevenlabs_apikey")


@lru_cache()
def get_settings():
    return Settings()
