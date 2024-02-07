import requests
import os
from constants import url
#from secret_constants import openai_key, proxy

openai_key = os.environ['OPENAI_KEY']
proxy = os.environ['PROXY']

def request_to_gpt(messages: [{"role": str,"content": str}]):
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
									"model": "gpt-3.5-turbo-1106", 
									"messages": messages, 
									"max_tokens": 250
								})
  return response