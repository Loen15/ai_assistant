from pyrogram import Client
from open_ai_api import request_to_gpt
from constants import prompt_for_redirect

def redirect(app: Client, username: str, self_id: int):
  app.send_message(self_id,f'''@{username} готов воспользоваться Вашими услугами''')
  content = ''
  for msg in app.get_chat_history(username):   
    if msg.from_user.is_self:
      content += 'а: ' + msg.text + '\n'
      if 'Вам нужна помощь военного юриста' in msg.text:
        break
    else:
      if msg.text is None and msg.caption is None:
        msg.forward(self_id)
        continue
      if msg.text is None:
        msg.forward(self_id)
        content += 'к: ' + msg.caption + '\n'
      else:
        content += 'к: ' + msg.text + '\n'
  msgs = [{"role": "system","content": prompt_for_redirect},{"role": "user","content": content}]
  res = request_to_gpt(msgs)
  res = res.json()
  app.send_message(self_id, str(res['choices'][0]['message']['content']))
