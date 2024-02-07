from pyrogram import Client
from constants import count_of_msgs




def generate_chat(app: Client, text: str, chat_id: int, prompt_for_ai: str, is_user: bool):
  msgs = [{"role": "system","content": prompt_for_ai}]
  msgs.append({"role": "user" if is_user else "assistant","content": text})
  for msg in app.get_chat_history(chat_id, offset = 1, limit = count_of_msgs):
    if msg.text ==  None and msg.caption == None: continue
    text = msg.text if msg.text !=  None else msg.caption
    if msg.from_user.is_self:
      msgs.insert(1,{"role": "assistant","content": text})
    else:
      msgs.insert(1,{"role": "user","content": text})
  return msgs