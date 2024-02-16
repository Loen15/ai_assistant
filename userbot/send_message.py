from pyrogram import Client
import os
from redirect import redirect
from conclusion_checker import is_conclusion

self_id = int(os.environ['SELF_ID'])

# функция парсинга и отправки сообщения от GPT или отправки уведомления Вам о том, что что-то пошло не так, в таком случае сам ответ от GPT отправится в избранные в аккаунте бота
def send_message(app: Client, username: str, response):
  try:    
    res = response.json()
    answer = str(res['choices'][0]['message']['content'])
    try:
      # если бот тупой и не понимает чот надо писать по одному вопросу и не нумеровать их (он тупой, так что эта строка нужна)
      app.send_message(username, answer[: answer.find('?') + 1].replace("1. ", ""))
    except:
      app.send_message(username, answer)
  except:
    app.send_message(self_id, f'''В чате с @{username} возникла ошибка''')
    try:
      app.send_message('me', f'''@{username}: {response.status_code} {res}''')  
    except:
      try:
        app.send_message('me', f'''@{username}: {str(response.content)}''')  
      except:
        app.send_message('me', f'''@{username}: 'непредвиденная ошибка''')
  # если бот написал {conclusion} (или как-то его перефразировал), то докладываем Вам об этом
  if is_conclusion(answer):
      redirect(app, username, self_id)
  
  # печатает затрачиваемые токены
  #print(res['usage'])
   