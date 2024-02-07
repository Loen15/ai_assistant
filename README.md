файл с константами (constants_example.py) переименовать, удалив '_example' в названии и заполнить необходимыми данными
  
заполнить переменные окружения в докере

собрать образ докера  
```docker build -t ai-assistant .```  
запустить контейнер  
```docker run -it --restart=unless-stopped --name my_assistant ai-assistant ```  

