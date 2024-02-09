from pyrogram import Client
import os
import time
from open_ai_api import request_to_gpt
from generator_of_msgs import generate_chat
from send_message import send_message
from constants import prompt_for_ai, prompt_for_ai_without_conlusion
#from secret_constants import api_id, api_hash
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
print(datetime.datetime.now())

app = Client("my_account", api_id, api_hash)

@app.on_message()
def log(client, message):
  
  # игнорируем свои сообщения и сообщения без текста
  if message.from_user.is_self or (message.text == None and message.caption == None): 
    return
  
  # добавил человечность, чтобы ответ приходил не сразу
  time.sleep(3)
  app.read_chat_history(message.chat.id)

  time.sleep(12)
  # проверяем не написал ли клиент что-то еще, 
  # если писал, то выходим из этого потока   
  for msg in app.get_chat_history(message.chat.id, limit = 1):
    if msg.caption == None and msg.text != message.text: return
    if msg.text == None and msg.caption != message.caption: return 
  
  # формируем начало диалога с GPT API из системной истории бота
  msgs = generate_chat(app, 
                       message.text if message.text != None else message.caption, 
                       message.chat.id, 
                       prompt_for_ai, True)

  # получаем ответ от GPT API 
  res = request_to_gpt(msgs)

  # проверяем не написал ли клиент что-то еще, 
  # если писал, то выходим из этого потока  
  for msg in app.get_chat_history(message.chat.id, limit = 1):
    if msg.caption == None and msg.text != message.text: return
    if msg.text == None and msg.caption != message.caption: return
  
  # отправляем ответ или пишем себе об ошибке  
  send_message(app, message.chat.username, res)  


def job():
  for dialog in app.get_dialogs():
    delta = datetime.datetime.now() - dialog.top_message.date
    if delta.total_seconds() // 3600 > 12:
      continue

    # напоминаем о себе если человек не отвечает больше 4 часов, но не рассматриваем чаты где последнее сообщение позднее 12 часов
    if dialog.top_message.from_user.is_self and 'в течение дня' not in dialog.top_message.text and 'заявка принята' not in dialog.top_message.text:
      if delta.total_seconds() // 3600 > 4:
        for msg in app.get_chat_history(dialog.chat.id, limit=1, offset=1):
          if not msg.from_user.is_self:
            content = ''
            for msg in app.get_chat_history(dialog.chat.id):   
              if msg.from_user.is_self:
                if msg.text == None and msg.caption == None:
                  continue
                content += 'а: ' + msg.caption if msg.text == None else msg.text + '\n'
              else:
                if msg.text == None and msg.caption == None:
                  continue
                content += 'к: ' + msg.caption if msg.text == None else msg.text + '\n'

            msgs = [{"role": "system","content": prompt_for_ai_without_conlusion},{"role": "user","content": content}]
            res = request_to_gpt(msgs)
            for msg in app.get_chat_history(dialog.chat.id, limit = 1):
              if msg.caption == None and msg.text != dialog.top_message.text: return
              if msg.text == None and msg.caption != dialog.top_message.caption: return
    
            send_message(app, dialog.chat.username, res)
    # если в течении 5 минут мы не написали человеку то пишем
    else:
      if not dialog.top_message.from_user.is_self and delta.total_seconds() // 60 > 5:
        msgs = generate_chat(app, 
                             dialog.top_message.text if dialog.top_message.text != None else dialog.top_message.caption, 
                             dialog.chat.id, 
                             prompt_for_ai, True)

        res = request_to_gpt(msgs)
        for msg in app.get_chat_history(dialog.chat.id, limit = 1):
          if msg.caption != None and msg.text != dialog.top_message.text: return
          if msg.text != None and msg.caption != dialog.top_message.caption: return

        send_message(app, dialog.chat.username, res)  

                              

scheduler = BackgroundScheduler()
scheduler.add_job(job, "interval", minutes = 45)


scheduler.start()      
app.run()
