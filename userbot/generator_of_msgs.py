from pyrogram import Client



# функция генерирующая чат для GPT
def generate_chat(app: Client, text: str, chat_id: int, prompt_for_ai: str, is_user: bool):
  # формируем список json обьектов для GPT
  #msgs = [{"role": "system","content": prompt_for_ai}]
  msgs = [{"role": "user" if is_user else "assistant","content": text}]
  for msg in app.get_chat_history(chat_id, offset = 1):
    if msg.text ==  None and msg.caption == None: continue
    text = msg.text if msg.text !=  None else msg.caption
    if msg.from_user.is_self:
      msgs.insert(0,{"role": "assistant","content": text})
    else:
      msgs.insert(0,{"role": "user","content": text})
  msgs.insert(-20,{"role": "system","content": prompt_for_ai})
  return msgs