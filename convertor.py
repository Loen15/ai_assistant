from pyrogram import Client
import json
from constants import prompt_for_ai, count_of_msgs



def convert_to_msgs(chat_id: int, text: str, app: Client):
  result = [
    {
      "role": "system",
      "content": prompt_for_ai
    }
  ]
  result.append({
      "role": "user",
      "content": text
    })
  for msg in app.get_chat_history(chat_id, limit = count_of_msgs, offset = 1):
    if msg.text ==  None and msg.caption == None: continue
    text = msg.text if msg.text !=  None else msg.caption
    if msg.from_user.is_self:
      result.insert(1,
                    {
                      "role": "assistant",
                      "content": text
                    })
    else:
      result.insert(1,
                    {
                      "role": "user",
                      "content": text
                    })
    
  return result

