from secret_constants import api_id, api_hash, self_id

from pyrogram import Client

from open_ai_api import request_to_gpt
from convertor import convert_to_msgs

app = Client("my_account", api_id, api_hash)

@app.on_message()
def log(client, message):
  
  if message.from_user.is_self or (message.text is None and message.caption is None): 
    return
  
  msgs = convert_to_msgs(message.chat.id, message.text if message.text != None else message.caption, app)

  res = request_to_gpt(msgs)

  for msg in app.get_chat_history(message.chat.id, limit = 1):
    if msg.caption is None and msg.text != message.text: return
    if msg.text is None and msg.caption != message.caption: return
  
  if 'choices' in res:
    app.send_message(message.chat.id, res['choices'][0]['message']['content'])
  else:
    try:
      app.send_message(self_id, res)
    except:
      if res.status_code == '403':
        app.send_message(self_id, 'включи vpn на хосте')
      else:
        app.send_message(self_id, 'непредвиденная ошибка')

app.run()
