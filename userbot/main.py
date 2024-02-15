from pyrogram import Client, enums
from pyrogram.raw import functions
import os
import time
from open_ai_api import request_to_gpt
from generator_of_msgs import generate_chat
from send_message import send_message
from conclusion_checker import is_conclusion
from constants import prompt_for_ai, prompt_for_ai_without_conlusion
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
#from secret_constants import api_id, api_hash

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']

# авторизуемся в telegram
app = Client("my_account", api_id, api_hash)

# триггер, вызывающий функцию log когда приходит сообщение
@app.on_message()
def log(client, message):
  
  # игнорируем свои сообщения и сообщения без текста
  if message.from_user.is_self or (message.text == None and message.caption == None): 
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
    if msg.caption == None and msg.text != message.text:  
      app.send_chat_action(message.chat.id, enums.ChatAction.CANCEL) 
      return
    if msg.text == None and msg.caption != message.caption:  
      app.send_chat_action(message.chat.id, enums.ChatAction.CANCEL) 
      return 
  
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
    if msg.caption == None and msg.text != message.text: 
      app.send_chat_action(message.chat.id, enums.ChatAction.CANCEL) 
      return
    if msg.text == None and msg.caption != message.caption:  
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
  
  # ставим статус онлайн
  app.invoke(functions.account.UpdateStatus(offline=False))
  
  # рассматриваем все диалоги
  for dialog in app.get_dialogs():
    # считаем сколько времени прошло и если болше 13 часов, то игнорируем данные диалоги (время ночью 7 часов, плюс 4 часа задержки)
    delta = datetime.datetime.now() - dialog.top_message.date
    if delta.total_seconds() // 3600 > 13:
      continue

    # напоминаем о себе если человек не отвечает больше 4 часов, но не рассматриваем чаты где последнее сообщение {conclusion}
    if dialog.top_message.from_user.is_self and not is_conclusion(dialog.top_message.text):
      if delta.total_seconds() // 3600 > 4:
        break_flag = False
        
        # Проверяем напоминал ли бот о себе
        for msg in app.get_chat_history(dialog.chat.id, limit=1, offset=1):
          if msg.from_user.is_self:
            break_flag = True
        if break_flag: continue

        content = ''

        # рассматриваем все сообщения в отдельном чате
        for msg in app.get_chat_history(dialog.chat.id):
          # не напоминаем о себе если уже связывали с человеком 
          if is_conclusion(msg.text):
            break_flag = True
            break 
          # формируем диалог для GPT
          if msg.from_user.is_self:
            if msg.text == None and msg.caption == None:
              continue
            content += 'а: ' + msg.caption if msg.text == None else msg.text + '\n'
          else:
            if msg.text == None and msg.caption == None:
              continue
            content += 'к: ' + msg.caption if msg.text == None else msg.text + '\n'
        # если уже связывали с человеком то выходим из этого чата
        if break_flag: continue
        # отправляем запрос к GPT и пишем ответ
        msgs = [{"role": "system","content": prompt_for_ai_without_conlusion},{"role": "user","content": content}]
        res = request_to_gpt(msgs)
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

                              
# настраиваем планировщик, чтобы он каждые 45 минут запускал функцию job
scheduler = BackgroundScheduler()
scheduler.add_job(job, "interval", minutes = 45)

# запускаем планировщик и бота
scheduler.start()      
app.run()
