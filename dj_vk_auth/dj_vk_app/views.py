import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from . import utils



CLIENT_ID = "7365067"
DJ_APP_NAME = "dj_vk_app"
DOMAIN = "44ec43aa-2e14-4ff1-ada3-d1b2e4418b0e.pub.cloud.scaleway.com:8000"


# Проверка в браузере клиента: переход по адресу http://<домен>/<имя приложения dj>/
def index(
    request, 
    domain=DOMAIN,
    dj_app_name=DJ_APP_NAME):

    """ Проверяет, регистрируется пользователь впервые или нет"""

    if 'testdj' not in request.COOKIES:
        return render(request, "dj_vk_app/home.html")
    else:
        return HttpResponseRedirect(f"http://{DOMAIN}/{DJ_APP_NAME}/login/")


# Не предусматривает случай при котором пользователь нажимает "Отмена"
# Проверка в браузере клиента: нажатие на кнопку "Авторизоваться"
def login(
    request,
    client_id_val=CLIENT_ID,
    domain=DOMAIN,
    dj_app_name=DJ_APP_NAME):

    """ Осуществляет перенаправление на сервер ВКонтакте для предоставления прав доступа к информации пользователя"""

    try:
        return HttpResponseRedirect(f"https://oauth.vk.com/authorize?client_id={CLIENT_ID}&scope=friends,offline&redirect_uri=http://{DOMAIN}/{DJ_APP_NAME}/final/&response_type=code")
    except:
        return HttpResponse("<h1 style='color:yellow'> Сервер ВКонтакте временно недоступен. Повторите попытку позднее. </h1>")


def final(request):
    """ Завершает авторизацию, выводит информацию об авторизованном пользователе и его друзьях"""
    url_for_code_search = request.build_absolute_uri()
    code = url_for_code_search[94:] # параметр для авторизации vk-приложения

    data = utils.get_info(code)
    access_token, user_id = data['access_token'], data['user_id']
    data = utils.get_info_1(user_id, access_token)
    first_name, last_name = data['response'][0]['first_name'], data['response'][0]['last_name']
    header = f"Здравствуйте, {first_name} {last_name}, Вы авторизованы.<br>"
    data = utils.get_info_2(access_token)
    array_of_friends_ID = data['response']['items']
    amount_of_friends = len(array_of_friends_ID)

    report = header + utils.create_text_about_friends(array_of_friends_ID, amount_of_friends, header, access_token)
    
    # Проверяет, регистрируется пользователь впервые или нет
    if 'testdj' not in request.COOKIES:
        response = HttpResponse(report)
        response.set_cookie('testdj', 'VK_auth', max_age=60*60*24*365*2) # если куки не обнаружены, то записываем их в браузер
    else:
        response = HttpResponse(report)
    return response