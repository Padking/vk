import json
import requests
import time



def get_info(code):
    request_link = f"https://oauth.vk.com/access_token?client_id=7365067&client_secret=ASWRHCQo7G76Klq1r019&redirect_uri=44ec43aa-2e14-4ff1-ada3-d1b2e4418b0e.pub.cloud.scaleway.com:8000/dj_vk_app/end/&code={code}"
    try:
        r = requests.get(url=request_link) 
    except:
        return "<h1 style='color:yellow'> Сервер ВКонтакте временно недоступен. Повторите попытку позднее. </h1>"
    return r.json()


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
        text = "Друзей в списке контактов нет<br>"
        return text
    else:
        tmp_lines = ''
        for i in range(num): 
            user_id = str(ids[i])
            time.sleep(0.2)
            data = get_info_1(user_id, key)
            first_name, last_name = data['response'][0]['first_name'], data['response'][0]['last_name']
            tmp_new_string = f"{first_name} {last_name}"
            new_string = f"<a href='https://vk.com/id{user_id}'>{tmp_new_string}</a><br>"
            tmp_lines += new_string
        if num < 5:
            text = "Меньше 5-ти друзей в списке контактов:<br>" + tmp_lines
        else:
            text = "5 друзей из списка контактов, выбранных в случайном порядке:<br>" + tmp_lines
        return text