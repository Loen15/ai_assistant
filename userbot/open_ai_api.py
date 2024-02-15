import requests
import os
from constants import url
#from secret_constants import openai_key, proxy

openai_key = os.environ['OPENAI_KEY']
proxy = os.environ['PROXY']

# функция, отправляющая POST запрос на сайт OpenAI
def request_to_gpt(messages):
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
									"max_tokens": 1000
								})
	return response