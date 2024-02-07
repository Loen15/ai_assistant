from pyrogram import Client
import os
from redirect import redirect
#from secret_constants import self_id

self_id = int(os.environ['SELF_ID'])

def send_message(app: Client, username: str, res):
  try:    
    res = res.json()
    answer = str(res['choices'][0]['message']['content'])
    if 'Ваша заявка принята' in  answer:
      redirect(app, username, self_id)
    try:
      app.send_message(username, answer[: answer.find('?') + 1])
    except:
      app.send_message(username, answer)
  except:
    try:
      app.send_message(self_id, res)  
    except:
      try:
        app.send_message(self_id, str(res.content))
      except:  
        app.send_message(self_id, 'непредвиденная ошибка')    