from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index , name='index'),
    url(r'^login/$', views.login , name='login'),
    url(r'^prend/$', views.prend , name='prend'),
    url(r'^user/$', views.user , name='user'),
    url(r'^logout_user/$', views.logout_user , name='logout_user')
]
