FROM python:3.10.0

WORKDIR /userbot
COPY . .

RUN apt update
RUN pip install --upgrade pip pyrogram requests tgcrypto pymongo

ENTRYPOINT ["python", "main.py"]