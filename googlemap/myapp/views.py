# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def backend (request):
    return render(request, "index.html")
def shousuo (request):
    return render(request, "shousuo.html")
def user_center (request):
    return render(request, "user_center.html")
def user_account (request):
    return render(request, "user_account.html")
def user_info (request):
    return render(request, "user_info.html")
def user_trade (request):
    return render(request, "user_trade.html")

