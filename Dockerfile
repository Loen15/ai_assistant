FROM python:3.10.0

WORKDIR /userbot
COPY ./userbot .

RUN apt update
RUN pip install --upgrade pip pyrogram requests tgcrypto apscheduler

ENV API_ID=... API_HASH=... SELF_ID=... OPENAI_KEY=... PROXY=... TZ=Europe/Moscow

ENTRYPOINT ["python", "main.py"]