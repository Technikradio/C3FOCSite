from django.http import HttpRequest
from django.shortcuts import redirect


def add_article_action(request: HttpRequest, default_foreward_url: str):
    forward_url = default_foreward_url
    # TODO fix
    return redirect(forward_url)


def create_reservation_action(request: HttpRequest):
    # TODO fix
    pass
