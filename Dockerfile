FROM python:3.10.0

WORKDIR /userbot
COPY ./userbot .

RUN apt update
RUN pip install --upgrade pip pyrogram requests tgcrypto apscheduler

ENTRYPOINT ["python", "main.py"]