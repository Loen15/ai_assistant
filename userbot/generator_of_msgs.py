from pyrogram import Client
from open_ai_api import request_to_gpt
from constants import prompt_for_redirect

# функция генерирующая чат для GPT
def generate_chat(app: Client, text: str, chat_id: int, prompt_for_ai: str, is_user: bool):
  # формируем список json обьектов для GPT
  msgs = [{"role": "user" if is_user else "assistant","content": text}]
  for msg in app.get_chat_history(chat_id, offset = 1, limit = 179):
    if msg.text ==  None and msg.caption == None: continue
    text = msg.text if msg.text !=  None else msg.caption
    if msg.from_user.is_self:
      msgs.insert(0,{"role": "assistant","content": text})
    else:
      msgs.insert(0,{"role": "user","content": text})
  if app.get_chat_history_count(chat_id) > 180:
    try:
      content = ''
      for msg in app.get_chat_history(chat_id, offset = 180):   
        if msg.from_user.is_self:
          if msg.text == None and msg.caption == None:
            continue
          content += 'а: ' + msg.text if msg.text != None else msg.caption + '\n'
        else:
          if msg.text == None and msg.caption == None:
            continue
          content += 'к: ' + msg.text if msg.text != None else msg.caption + '\n'
      msgs_180 = [{"role": "system","content": prompt_for_redirect},{"role": "user","content": content}]
      response = request_to_gpt(msgs_180)
      res = response.json()
      msgs.insert(0,{"role": "user","content": str(res['choices'][0]['message']['content'])})
    except:
      app.send_message('me', f'''В чате с @{chat_id} возникла ошибка при конвертировании чата в одно сообщение''') 
  msgs.insert(-20,{"role": "system","content": prompt_for_ai})
  return msgs