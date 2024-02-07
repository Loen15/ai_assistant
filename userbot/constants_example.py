# адрес куда направляется POST-запрос
url = 'https://api.openai.com/v1/chat/completions'
# количество старых сообщений, которые будет "помнить" GPT AI
count_of_msgs = 1
# Фраза остановки
conclusion = 'конец'
# легенда для бота
prompt_for_ai =  'ты ассистент, помогай, когда помог напиши дословно {conclusion}'
# легенда для напоминалки о себе
prompt_for_ai_without_conlusion = 'ты ассистент, помогай'
