import requests
from constants import url
from secret_constants import openai_key

def request_to_gpt(messages: [{
                      "role": str,
                      "content": str
                    }]):
	response = requests.post(url,
								headers={
									"Content-Type": "application/json", 
									"Authorization": "Bearer " + openai_key,
								},
								json = 
								{
									"model": "gpt-3.5-turbo-1106", 
									"messages": messages, 
									"max_tokens": 200, 
									"temperature": 1
								}
	)
	try:
		return response.json()
	except:
		return response