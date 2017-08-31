from django.http import HttpRequest, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import redirect
from . import page_skeleton, magic
from .form import Form, TextField, PlainText, TextArea, SubmitButton, NumberField
from ..models import Profile


def render_edit_page(http_request: HttpRequest, action_url: str):
    user_id = None
    profile = None
    if http_request.GET.get("user_id"):
        post_id = int(http_request.GET["user_id"])
    if user_id is not None:
        profile = Profile.objects.get(pk=user_id)
    pass


def action_save_user(request: HttpRequest, default_forward_url: str = ".."):
    """
    This functions saves the changes to the user or adds a new one. It completely creates the Httpresponse
    :param request: the HttpRequest
    :param default_forward_url: The URL to forward to if nothing was specified
    :return: The crafted HttpResponse
    """
    pass
