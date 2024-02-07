from pyrogram import Client
import os
#from secret_constants import self_id

self_id = int(os.environ['SELF_ID'])

def send_message(app: Client, chat_id: int, res):
  try:    
    res = res.json()
    answer = str(res['choices'][0]['message']['content'])
    try:
      app.send_message(chat_id, answer[: answer.find('?') + 1])
    except:
      app.send_message(chat_id, answer)
  except:
    try:
      app.send_message(self_id, str(res.content))
    except:
      app.send_message(self_id, 'непредвиденная ошибка')    