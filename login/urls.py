#encoding=utf-8
__author__ = 'Administrator'

from django.urls import re_path
from django.conf.urls import include
from . import views


app_name = 'login'
#?P<question_id>则表示我要给这个捕获的值指定一个特殊的变量名，
# 在视图中可以通过question_id这个变量名随意的引用它，形成一个关键字参数，不用考虑参数的位置。
urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^index/$', views.index),
    re_path(r'^login/$', views.login),
    re_path(r'^register/$', views.register),
    re_path(r'^logout/$', views.logout),
    re_path(r'^confirm/$', views.user_confirm),

]