#encoding=utf-8
__author__ = 'Administrator'

#from django.conf.urls import url
from django.urls import re_path
from . import  views

app_name = 'polls'
#?P<question_id>则表示我要给这个捕获的值指定一个特殊的变量名，
# 在视图中可以通过question_id这个变量名随意的引用它，形成一个关键字参数，不用考虑参数的位置。
urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    re_path(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    re_path(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]