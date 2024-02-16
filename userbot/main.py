from pyrogram import Client, enums, filters
import os
import time
from open_ai_api import request_to_gpt
from generator_of_msgs import generate_chat
from send_message import send_message
from checker import is_conclusion, message_to_text
from constants import prompt_for_ai, prompt_for_ai_without_conlusion
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']

# авторизуемся в telegram
app = Client("my_account", api_id, api_hash)

# ответ на аудио
@app.on_message(filters.voice & filters.incoming)
def log(client, message):
    app.read_chat_history(message.chat.id)
    app.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    time.sleep(3)
    msg = app.send_message(message.chat.id, 'Прошу прощения, но у меня сейчас нет возможности прослушать Ваше сообщение, не могли бы Вы написать то о чем говорили в аудио?')
    app.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)
    app.delete_messages(message.chat.id, msg.id, revoke=False)

# ответ на видео
@app.on_message(filters.video_note & filters.incoming)
def log(client, message):
    app.read_chat_history(message.chat.id)
    app.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    time.sleep(3)
    msg = app.send_message(message.chat.id, 'Прошу прощения, но у меня сейчас нет возможности просмотреть Ваше сообщение, не могли бы Вы написать то о чем говорили в видео?')
    app.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)
    app.delete_messages(message.chat.id, msg.id, revoke=False)

# ответ на сообщения
@app.on_message()
def log(client, message):
  # игнорируем свои сообщения (не в фильтре так как ловит сообщения в избранном)
  if message.from_user.is_self: 
    return
  
  # добавил человечность, чтобы ответ приходил не сразу 
  time.sleep(2)
  app.read_chat_history(message.chat.id) # и дополнительно отмечаем сообщение прочитанным через 3 секунды
  time.sleep(1)
  app.send_chat_action(message.chat.id, enums.ChatAction.TYPING) # делаем вид что пишем
  time.sleep(6)
  app.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
  time.sleep(6)
  app.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
  # проверяем не написал ли клиент что-то еще, 
  # если писал, то выходим из этого потока   
  for msg in app.get_chat_history(message.chat.id, limit = 1):
    if msg.id != message.id:  
      app.send_chat_action(message.chat.id, enums.ChatAction.CANCEL) 
      return
  
  # формируем начало диалога с GPT API из системной истории бота
  msgs = generate_chat(app, 
                       message_to_text(message), 
                       message.chat.id, 
                       prompt_for_ai, True)

  # получаем ответ от GPT API 
  res = request_to_gpt(msgs)

  # проверяем не написал ли клиент что-то еще, 
  # если писал, то выходим из этого потока  
  for msg in app.get_chat_history(message.chat.id, limit = 1):
    if msg.id != message.id:  
      app.send_chat_action(message.chat.id, enums.ChatAction.CANCEL) 
      return
  
  #перестаем писать
  app.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)
  # отправляем ответ или пишем себе об ошибке  
  send_message(app, message.chat.username, res)  


def job():
  # не пишем с 12 ночи до 7 утра (касается напоминай о себе и проеба в коде, когда бот не ответил самостоятельно)
  if datetime.datetime.now().time() < datetime.time(7,0,0,0):
    return
  
  # рассматриваем все диалоги
  for dialog in app.get_dialogs():
    # считаем сколько времени прошло и если болше 13 часов, то игнорируем данные диалоги (время ночью 7 часов, плюс 4 часа задержки)
    delta = datetime.datetime.now() - dialog.top_message.date
    if delta.total_seconds() // 3600 > 14:
      continue

    # напоминаем о себе если человек не отвечает больше 4 часов, но не рассматриваем чаты где последнее сообщение {conclusion}
    if dialog.top_message.from_user.is_self and not is_conclusion(message_to_text(dialog.top_message)):
      if delta.total_seconds() // 3600 < 4:
        continue
      break_flag = False
        
      # Проверяем напоминал ли бот о себе
      for msg in app.get_chat_history(dialog.chat.id, limit=1, offset=1):
        if msg.from_user.is_self:
          break_flag = True
      if break_flag: continue

      content = ''

      # рассматриваем все сообщения в отдельном чате
      for msg in app.get_chat_history(dialog.chat.id):
        # формируем диалог для GPT
        if msg.from_user.is_self:
          content += 'а: ' + message_to_text(msg) + '\n'
        else:
          content += 'к: ' + message_to_text(msg) + '\n'
      # отправляем запрос к GPT и пишем ответ
      msgs = [{"role": "system","content": prompt_for_ai_without_conlusion},{"role": "user","content": content}]
      res = request_to_gpt(msgs)
      send_message(app, dialog.chat.username, res)
    # если в течении 5 минут мы не написали человеку то пишем
    else:
      if not dialog.top_message.from_user.is_self and delta.total_seconds() // 60 > 5:
        msgs = generate_chat(app, 
                             message_to_text(dialog.top_message), 
                             dialog.chat.id, 
                             prompt_for_ai, True)

        res = request_to_gpt(msgs)

        send_message(app, dialog.chat.username, res)  

                              
# настраиваем планировщик, чтобы он каждые 45 минут запускал функцию job
scheduler = BackgroundScheduler()
scheduler.add_job(job, "interval", minutes = 45)

# запускаем планировщик и бота
scheduler.start()      
app.run()
