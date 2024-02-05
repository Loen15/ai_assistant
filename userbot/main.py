from pyrogram import Client, filters
import os
import time
from pymongo import MongoClient
from open_ai_api import request_to_gpt
from constants import prompt_for_ai, count_of_msgs
#from secret_constants import api_id, api_hash, self_id
from user_list import UserList

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
self_id = int(os.environ['SELF_ID'])

app = Client("my_account", api_id, api_hash)

mongodb_host = os.environ.get('MONGO_HOST', 'mongo')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)
user_list = UserList(client)

@app.on_message(filters.text | filters.caption | filters.chat())
def log(client, message):
  
  # игнорируем свои сообщения и сообщения без текста
  if message.from_user.is_self or user_list.is_banned(message.from_user.username): 
    return
  
  # добавил человечность, чтобы ответ приходил не сразу
  #time.sleep(10)

  # формируем начало диалога с GPT API из системной истории бота
  msgs = [{"role": "system","content": prompt_for_ai}]
  
  # проверяем не написал ли клиент что-то еще, 
  # если писал, то выходим из этого потока   
  for msg in app.get_chat_history(message.chat.id, limit = 1):
    if msg.caption is None and msg.text != message.text: return
    if msg.text is None and msg.caption != message.caption: return 
    text = msg.text if msg.text !=  None else msg.caption
    msgs.append({"role": "user","content": text})
  
  # формируем диалог для GPT API
  for msg in app.get_chat_history(message.chat.id, offset = 1, limit = count_of_msgs):
    if msg.text ==  None and msg.caption == None: continue
    text = msg.text if msg.text !=  None else msg.caption
    if msg.from_user.is_self:
      msgs.insert(1,{"role": "assistant","content": text})
    else:
      msgs.insert(1,{"role": "user","content": text})

  # получаем ответ от GPT API 
  res = request_to_gpt(msgs)

  # проверяем не написал ли клиент что-то еще, 
  # если писал, то выходим из этого потока  
  for msg in app.get_chat_history(message.chat.id, limit = 1):
    if msg.caption is None and msg.text != message.text: return
    if msg.text is None and msg.caption != message.caption: return
  
  # отправляем ответ или пишем себе об ошибке  
  if 'choices' in res:
    answer = str(res['choices'][0]['message']['content'])
    try:
      app.send_message(message.chat.id, answer[: answer.find('?') + 1])
    except:
      app.send_message(message.chat.id, answer)
  else:
    try:
      app.send_message(self_id, res)
    except:
      if res.status_code == '403':
        app.send_message(self_id, 'включи vpn на хосте')
      else:
        if 'Sorry, you have been blocked' in str(res.content):
          app.send_message(self_id, 'прокси заблокировали')  
        else:
          try:
            app.send_message(self_id, str(res.content))
          except:
            app.send_message(self_id, 'непредвиденная ошибка')
        

app.run()
