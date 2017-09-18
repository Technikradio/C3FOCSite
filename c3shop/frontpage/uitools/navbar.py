from ..models import Settings
from django.http import HttpRequest
import json

NAV_BAR_SETTINGS_KEY: str = "frontpage.ui.navbar.content"


def process_link(position: int, item):
    return '<a href="' + item.get('href') + '">' + item.get('text') + '</a>'


def render_nav_bar(request: HttpRequest):
    try:
        feature_line: str = Settings.objects.find(SName=NAV_BAR_SETTINGS_KEY).property
        parts = json.loads(feature_line)
        a = '<div class="nav">'
        pos = -1
        for item in parts:
            pos += 1
            if str(item.get('type')) == "link":
                a += process_link(pos, item)
        a += '</div>'
        return a
    except:
        return "<h3>An error was thrown resulting in the incapability to display the nav bar</h3>"
