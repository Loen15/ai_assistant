файл с константами (constants_example.py) переименовать, удалив '_example' в названии и заполнить необходимыми данными

собрать образ докера  
```docker build -t ai-assistant .```  
запустить контейнер  
```docker run -it --restart=unless-stopped --name my_assistant -e API_ID=1234 -e API_HASH=d3f3fd3s8s9 -e SELF_ID=321 -e OPENAI_KEY=sk-jV5H8hH7D -e PROXY=http://user:password@host:port ai-assistant ```  
  
# Переменные окружения (пример)
данные аккаунта (отсюда -> https://my.telegram.org/auth)  
```-e API_ID=1234```  
```-e API_HASH=d3f3fd3s8s9```  
id аккаунта куда будут направляться сообщения об ошибках
```-e SELF_ID=321```  
ключ доступа к openAI API  
```-e OPENAI_KEY=sk-jV5H8hH7D```  
прокси для доступа openAI в России  
```-e PROXY =http://user:password@host:port```


