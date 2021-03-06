from django.http import HttpRequest
from django.template.context_processors import csrf


def get_csrf_form_element(request: HttpRequest):
    csrf_token = ""
    if request is not None:
        csrf_token = str(csrf(request)['csrf_token'])  # , 'utf-8')
    return '<div style="display:none"><input type="hidden" name="csrfmiddlewaretoken" value="' + csrf_token + \
           '"/></div>'
