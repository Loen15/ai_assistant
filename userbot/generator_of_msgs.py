from pyrogram import Client
from open_ai_api import request_to_gpt
from checker import message_to_text
from constants import prompt_for_redirect

# функция генерирующая чат для GPT
def generate_chat(app: Client, text: str, chat_id: int, prompt_for_ai: str, is_user: bool):
  # формируем список json обьектов для GPT
  msgs = [{"role": "user" if is_user else "assistant","content": text}]
  for msg in app.get_chat_history(chat_id, offset = 1, limit = 179):
    msgs.insert(0,{"role": "assistant" if msg.from_user.is_self else "user","content": message_to_text(msg)})  
  if app.get_chat_history_count(chat_id) > 180:
    try:
      content = ''
      for msg in app.get_chat_history(chat_id, offset = 180):   
        content += 'а: ' if msg.from_user.is_self else 'к: ' + message_to_text(msg) + '\n'
      msgs_180 = [{"role": "system","content": prompt_for_redirect},{"role": "user","content": content}]
      response = request_to_gpt(msgs_180)
      res = response.json()
      msgs.insert(0,{"role": "user","content": str(res['choices'][0]['message']['content'])})
    except:
      app.send_message('me', f'''В чате с @{chat_id} возникла ошибка при конвертировании старых сообщений в одно''') 
  msgs.insert(-20,{"role": "system","content": prompt_for_ai})
  return msgs