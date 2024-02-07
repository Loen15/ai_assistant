from pyrogram import Client
import os
import time
from open_ai_api import request_to_gpt
from generator_of_msgs import generate_chat
from send_message import send_message
from constants import prompt_for_ai, promt_for_ai_reminder
# from secret_constants import api_id, api_hash
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']

app = Client("my_account", api_id, api_hash)

@app.on_message()
def log(client, message):
  
  # игнорируем свои сообщения и сообщения без текста
  if message.from_user.is_self or (message.text is None and message.caption is None): 
    return
  
  # добавил человечность, чтобы ответ приходил не сразу
  time.sleep(10)

  # проверяем не написал ли клиент что-то еще, 
  # если писал, то выходим из этого потока   
  for msg in app.get_chat_history(message.chat.id, limit = 1):
    if msg.caption is None and msg.text != message.text: return
    if msg.text is None and msg.caption != message.caption: return 
  
  # формируем начало диалога с GPT API из системной истории бота
  msgs = generate_chat(app, 
                       message.text if message.text is not None else message.caption, 
                       message.chat.id, 
                       prompt_for_ai, True)

  # получаем ответ от GPT API 
  res = request_to_gpt(msgs)

  # проверяем не написал ли клиент что-то еще, 
  # если писал, то выходим из этого потока  
  for msg in app.get_chat_history(message.chat.id, limit = 1):
    if msg.caption is None and msg.text != message.text: return
    if msg.text is None and msg.caption != message.caption: return
  
  # отправляем ответ или пишем себе об ошибке  
  send_message(app, message.chat.id, res)  


def job():
  for dialog in app.get_dialogs():
    delta = datetime.datetime.now() - dialog.top_message.date
    # напоминаем о себе если человек не отвечает больше 4 часов, но не рассматриваем чаты где последнее сообщение позднее 12 часов
    if dialog.top_message.from_user.is_self:
      if delta.total_seconds() // 3600 > 4 and delta.total_seconds() // 3600 < 12:
        for msg in app.get_chat_history(dialog.chat.id, limit=1, offset=1):
          if not msg.from_user.is_self:
            res = request_to_gpt([{"role": "user","content": promt_for_ai_reminder}])
            send_message(app, dialog.chat.id, res)
    # если в течении 5 минут мы не написали человеку то пишем
    else:
      if delta.total_seconds() // 60 > 5:
        msgs = generate_chat(app, 
                             dialog.top_message.text if dialog.top_message.text is not None else dialog.top_message.caption, 
                             dialog.chat.id, 
                             prompt_for_ai, True)

        res = request_to_gpt(msgs)

        for msg in app.get_chat_history(dialog.chat.id, limit = 1):
          if msg.caption is None and msg.text != dialog.top_message.text: return
          if msg.text is None and msg.caption != dialog.top_message.caption: return

        send_message(app, dialog.chat.id, res)  

                              

scheduler = BackgroundScheduler()
scheduler.add_job(job, "interval", minutes = 30)


scheduler.start()      
app.run()
