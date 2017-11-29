from ..models import Settings
from django.http import HttpRequest
import json

NAV_BAR_SETTINGS_KEY: str = "frontpage.ui.navbar.content"


def process_link(position: int, item):
    css_class: str = "w3-bar-item w3-button w3-hide-small w3-hover-white"
    if position == 0:
        css_class = "w3-bar-item w3-button w3-theme-l1"
    return '<a href="' + item.get('href') + '" class="' + css_class + '">' + \
            item.get('text') + '</a>'


def render_nav_bar(request: HttpRequest):
    try:
        feature_line: str = Settings.objects.get(SName=NAV_BAR_SETTINGS_KEY).property
        parts = json.loads(feature_line)
        a = '<div class="w3-top"><div class="w3-bar w3-theme w3-top w3-left-align w3-large">'
        pos = -1
        for item in parts:
            pos += 1
            if str(item.get('type')) == "link":
                a += process_link(pos, item) + " "
        if request.user.is_authenticated():
            a += '<a href="/admin/" class="w3-bar-item w3-button w3-hide-small w3-hover-white">Admin area</a>'
        else:
            a += '<a href="/login/?next=' + request.path + '" class="w3-bar-item w3-button w3-hide-small w3-hover-white">Login</a>'
        a += '</div></div>'
        return a
    except Exception as e:
        return "<h3>An error was thrown resulting in the incapability to display the nav bar:</h3>" + str(e)
