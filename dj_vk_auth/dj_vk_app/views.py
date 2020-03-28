import requests

from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from . import utils



CLIENT_ID = "7365067"
CLIEND_SECRET = "ASWRHCQo7G76Klq1r019"
DJ_APP_NAME = "dj_vk_app"
DOMAIN = "44ec43aa-2e14-4ff1-ada3-d1b2e4418b0e.pub.cloud.scaleway.com:8000"



def index(
    request, 
    domain=DOMAIN,
    dj_app_name=DJ_APP_NAME):

    """ Проверяет, регистрируется пользователь впервые или нет"""

    if 'testdj' not in request.COOKIES:
        return render(request, "dj_vk_app/home.html")
    else: # пользователь уже зарегистрирован
        return HttpResponseRedirect(f"http://{DOMAIN}/{DJ_APP_NAME}/login/")


def login(
    request,
    client_id_val=CLIENT_ID,
    domain=DOMAIN,
    dj_app_name=DJ_APP_NAME):

    """ Осуществляет перенаправление на сервер ВКонтакте для предоставления прав доступа к информации пользователя"""

    try:
        return HttpResponseRedirect(f"https://oauth.vk.com/authorize?client_id={CLIENT_ID}&scope=friends,offline&redirect_uri=http://{DOMAIN}/{DJ_APP_NAME}/prend/&response_type=code") # Запрос для открытия диалога авторизации согласно документации ВКонтакте
    except:
        return HttpResponse("<h1 style='color:yellow'> Сервер ВКонтакте временно недоступен. Повторите попытку позднее. </h1>")


def prend(
    request,
    client_id_val=CLIENT_ID,
    client_secret=CLIEND_SECRET,
    domain=DOMAIN,
    dj_app_name=DJ_APP_NAME):

    """ Перенаправляет на получение ключа доступа"""

    url_for_code_search = request.build_absolute_uri()
    start = url_for_code_search.find('code=') + len('code=')
    code = url_for_code_search[start:] # параметр для авторизации vk-приложения
    request_link = f"https://oauth.vk.com/access_token?client_id={CLIENT_ID}&client_secret={CLIEND_SECRET}&redirect_uri={DOMAIN}/{DJ_APP_NAME}/prend/&code={code}"
    try:
        r = requests.get(url=request_link)
        data = r.json()
        access_token, user_id = data['access_token'], data['user_id']
        return HttpResponseRedirect(f"http://{DOMAIN}/{DJ_APP_NAME}/user/?user_id={user_id}&access_token={access_token}")
    except:
        return "<h1 style='color:yellow'> Сервер ВКонтакте временно недоступен. Повторите попытку позднее. </h1>"


def user(request):
    """ Выводит информацию об авторизованном пользователе и его друзьях"""

    user_id = request.GET.get("user_id", 1)
    access_token = request.GET.get("access_token", "Proba")
    data = utils.get_info_1(user_id, access_token)
    first_name, last_name = data['response'][0]['first_name'], data['response'][0]['last_name']
    headline = f"Здравствуйте, {first_name} {last_name}, Вы авторизованы"
    data = utils.get_info_2(access_token)
    array_of_friends_ID = data['response']['items']
    amount_of_friends = len(array_of_friends_ID)
    subheadline, friend_names = utils.create_text_about_friends(array_of_friends_ID, amount_of_friends, headline, access_token)
    report = list(zip(array_of_friends_ID, friend_names))
    d = {"headline": headline, "subheadline": subheadline, "strings": report}
    if 'testdj' not in request.COOKIES:
        response = render(request, "dj_vk_app/out.html", context=d)
        response.set_cookie('testdj', 'VK_auth', max_age=60*60*24*365*2) # если куки не обнаружены, то записываем их в браузер
    else:
        response = render(request, "dj_vk_app/out.html", context=d)
    return HttpResponse(response)


def logout_user(
    request,
    domain=DOMAIN,
    dj_app_name=DJ_APP_NAME):

    """ Отменяет регистрацию пользователя"""

    logout(request)
    response = HttpResponseRedirect(f"http://{DOMAIN}/{DJ_APP_NAME}/")
    response.delete_cookie('testdj')
    return response