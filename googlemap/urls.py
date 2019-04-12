# -*- coding:utf-8 -*-
"""googlemap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from myapp import views
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index', views.backend, name='index'),
    url(r'^shousuo', views.shousuo, name='shousuo'),
    url(r'^user_account', views.user_account, name='user_account'),
    url(r'^user_center', views.user_center, name='user_center'),
    url(r'^user_info', views.user_info, name='user_info'),
    url(r'^user_trade', views.user_trade, name='user_trade'),
    url(r'^search', views.search, name='search'),
    # document_root为工程的文件夹目录
    url(r'^static/(?P<path>.*)$', serve, {'document_root': 'C:\Users\hptue\Desktop\googlemap\static'})
]
