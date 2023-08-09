FROM python:3.10.6-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt update && apt install build-essential -y && pip install --upgrade pip && pip install -r requirements.txt

CMD ["python3", "./main.py"]
