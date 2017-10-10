from django.http import HttpRequest
from django.shortcuts import redirect


def add_article_action(request: HttpRequest, default_foreward_url:str):
    forward_url = default_foreward_url

    return redirect(forward_url)
