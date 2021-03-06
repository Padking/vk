import json
import requests
import time



def get_info_1(user_id, access_token):
    request_link = f"https://api.vk.com/method/users.get?user_ids={user_id}&fields=bdate&access_token={access_token}&v=5.103"
    try:
        r = requests.get(url=request_link)
    except:
        return "<h1 style='color:yellow'> Сервер ВКонтакте временно недоступен. Повторите попытку позднее. </h1>"
    return r.json()


def get_info_2(access_token):
    request_link = f"https://api.vk.com/method/friends.get?order=random&count=5&access_token={access_token}&v=5.103" # ограничили количество выводимых друзей
    try:
        r = requests.get(url=request_link)
    except:
        return "<h1 style='color:yellow'> Сервер ВКонтакте временно недоступен. Повторите попытку позднее. </h1>"
    return r.json()


def create_text_about_friends(ids, num, text, key):
    """ Формирует текст с информацией о друзьях пользователя
    :param ids: id пользователей
    :param num: количество пользователей
    """
    if num == 0: # друзей нет
        first_line = "Друзей в списке контактов нет\n"
        other_lines = '\n'
        return first_line, other_lines.split('\n')
    else:
        other_lines = ''
        for i in range(num): 
            user_id = str(ids[i])
            time.sleep(0.2)
            data = get_info_1(user_id, key)
            first_name, last_name = data['response'][0]['first_name'], data['response'][0]['last_name']
            new_line = f"{first_name} {last_name} \n"
            other_lines += new_line
        if num < 5:
            first_line = "Меньше 5-ти друзей в списке контактов:\n"
            return first_line, other_lines.split('\n')
        else:
            first_line = "5 друзей из списка контактов, выбранных в случайном порядке:\n"
            return first_line, other_lines.split('\n')