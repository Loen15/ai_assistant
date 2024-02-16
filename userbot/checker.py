from constants import conclusion_list

# функция, проверяющая строку на то является ли она заколючением 
def is_conclusion(str):
  for conclusion in conclusion_list:
    if conclusion in str: return True
  return False

def message_to_text(message):
  if message.text != None:
    return message.text 
  if message.caption != None:
    return message.caption
  match message.media:
    case 'MessageMediaType.STICKER':
      return message.sticker.emoji
    case 'MessageMediaType.PHOTO':
      return 'Отправил Вам фото документа'
    case 'MessageMediaType.DOCUMENT':
      return 'Отправил Вам документ'
    case 'MessageMediaType.AUDIO':
      return 'Отправил Вам аудиофайл' 
    case 'MessageMediaType.VIDEO':
      return 'Отправил Вам видео'
    case 'MessageMediaType.ANIMATION':
      return 'Отправил Вам гифку'
    case 'MessageMediaType.CONTACT':
      return 'Отправил Вам контакт'
    case 'MessageMediaType.LOCATION':
      return 'Отправил Вам локацию'
    case 'MessageMediaType.VENUE':
      return 'Отправил Вам место проведения'
    case 'MessageMediaType.POLL':
      return 'Отправил Вам опрос'
    case 'MessageMediaType.WEB_PAGE':
      return 'Отправил Вам ссылку'
#    case 'MessageMediaType.DICE':
#    case 'MessageMediaType.GAME':
    case _:
      return ' '
  