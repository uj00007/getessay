
from django.conf.urls import url, include
from django.contrib import admin
from home import views


app_name = 'home'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^essaysuc/$',views.essaysuc,name='essaysuc'),

]
