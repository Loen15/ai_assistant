from pyrogram import Client
import os
from constants import conclusion
from open_ai_api import request_to_gpt
from convertor import convert_to_msgs

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
self_id = int(os.environ['SELF_ID'])

app = Client("my_account", api_id, api_hash)

@app.on_message()
def log(client, message):
  
  if message.from_user.is_self or (message.text is None and message.caption is None): 
    if message.text == conclusion:
      app.send_message(self_id, f"@{message.from_user.username} согласен на консультацию")
    return
  
  msgs = convert_to_msgs(message.chat.id, message.text if message.text != None else message.caption, app)

  res = request_to_gpt(msgs)

  for msg in app.get_chat_history(message.chat.id, limit = 1):
    if msg.caption is None and msg.text != message.text: return
    if msg.text is None and msg.caption != message.caption: return
  
  if 'choices' in res:
    answer = res['choices'][0]['message']['content']
    app.send_message(message.chat.id, answer)
  else:
    try:
      app.send_message(self_id, res)
    except:
      if res.status_code == '403':
        app.send_message('me', 'включи vpn на хосте')
      else:
        if 'Sorry, you have been blocked' in str(res.content):
          app.send_message('me', 'прокси заблокировали')  
        else: 
          app.send_message('me', 'непредвиденная ошибка')
        

app.run()
