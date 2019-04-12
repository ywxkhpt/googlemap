# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from search.twitter_search.run import run as twitter_search
from search.facebook_search.run import run as facebook_search
from search.google_search.run import run as google_search
from search.linkedin_search.run import run as linkedin_search


# Create your views here.

def backend(request):
    return render(request, "index.html")


def shousuo(request):
    return render(request, "shousuo.html")


def user_center(request):
    return render(request, "user_center.html")


def user_account(request):
    return render(request, "user_account.html")


def user_info(request):
    return render(request, "user_info.html")


def user_trade(request):
    return render(request, "user_trade.html")


def search(request):
    person_name = ""
    search_result = {}
    if request.POST:
        person_name = request.POST['personName']
    search_result["result"] = twitter_search(person_name)
    return render(request, "search_result_twitter.html", search_result)
