
from django.conf.urls import url, include
from django.contrib import admin

import home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^',include('home.urls')),
]
