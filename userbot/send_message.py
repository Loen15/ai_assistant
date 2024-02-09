from pyrogram import Client
import os
from redirect import redirect
import datetime
#from secret_constants import self_id

self_id = int(os.environ['SELF_ID'])

def send_message(app: Client, username: str, res):
  try:    
    res = res.json()
    answer = str(res['choices'][0]['message']['content'])
    try:
      app.send_message(username, answer[: answer.find('?') + 1])
    except:
      app.send_message(username, answer)
  except:
    app.send_message(self_id, f'''В чате с @{username} возникла ошибка''')
    try:
      app.send_message('me', f'''@{username} {datetime.datetime.now()}: {res}''')  
    except:
      try:
        app.send_message('me', f'''@{username} {datetime.datetime.now()}: {str(res.content)}''')  
      except:
        app.send_message('me', f'''@{username} {datetime.datetime.now()}: 'непредвиденная ошибка''')
  if 'в течение дня' in  answer:
      redirect(app, username, self_id)
   