from pyrogram import Client
import os
from redirect import redirect
import datetime
#from secret_constants import self_id

self_id = int(os.environ['SELF_ID'])

# функция парсинга и отправки сообщения от GPT или отправки уведомления Вам о том, что что-то пошло не так, в таком случае сам ответ от GPT отправится в избранные в аккаунте бота
def send_message(app: Client, username: str, res):
  try:    
    res = res.json()
    answer = str(res['choices'][0]['message']['content'])
    try:
      # если бот тупой и не понимает чот надо писать по одному вопросу и не нумеровать их (он тупой, так что эта строка нужна)
      app.send_message(username, answer[: answer.find('?') + 1].replace("1. ", ""))
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
  # если бот написал {conclusion} (или как-то его перефразировал), то докладываем Вам об этом
  if 'в течение дня' in  answer or 'заявка принята' in answer:
      redirect(app, username, self_id)
  
  # печатает затрачиваемые токены
  #print(res['usage'])
   