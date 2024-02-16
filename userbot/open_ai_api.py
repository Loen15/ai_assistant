import requests
import os
from random import randint
from time import sleep
from constants import url
#from secret_constants import openai_key, proxy

openai_key = os.environ['OPENAI_KEY']
proxy = os.environ['PROXY']

# функция, отправляющая POST запрос на сайт OpenAI
def request_to_gpt(messages):
	for i in range(1, 6):
		response = requests.post(url,
								headers={
									"Content-Type": "application/json", 
									"Authorization": "Bearer " + openai_key,
								},
								proxies = {
                  'https': proxy
								},
								json = 
								{
									"model": "gpt-3.5-turbo-0125", 
									"messages": messages,
									"temperature": 0,
									"max_tokens": 800
								})
		# если нормальный ответ пришел, то выходим 
		if response.status_code == 200:
			break
		# если ошибка в ключе или в авторизации, то выходим (дальше уже напишем об этом self_id)
		if response.status_code == 401:
			break
		# если закончились деньги на аккаунте, то выходим (дальше уже напишем об этом self_id)
		if response.status_code == 429 and 'current quota' in response.json()['error']['message']:
			break
		sleep(i * randint(20,60))
	
	return response