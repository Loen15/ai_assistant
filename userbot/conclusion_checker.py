from constants import conclusion_list

# функция, проверяющая строку на то является ли она заколючением 
def is_conclusion(str):
  for conclusion in conclusion_list:
    if conclusion in str: return True
  return False