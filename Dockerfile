FROM python:3.10.0

WORKDIR /back
COPY ./back .

RUN apt update
RUN pip install --upgrade pip pyrogram requests tgcrypto

ENTRYPOINT ["python", "main.py"]