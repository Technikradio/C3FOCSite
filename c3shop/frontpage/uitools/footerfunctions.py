from ..models import Settings
from django.http import HttpRequest
import json

FOOTER_SETTINGS_KEY: str = "frontpage.ui.footer.content"


def process_link(position: int, item):
    if position % 3 == 0:
        return '<a href="' + item.get('href') + '">' + item.get('text') + '</a><br />'
    else:
        return '<a href="' + item.get('href') + '">' + item.get('text') + '</a>'


def render_footer(http_request: HttpRequest):
    a = '<br/></div><footer class="w3-container w3-theme-l1">'
    try:
        feature_line: str = Settings.objects.get(SName=FOOTER_SETTINGS_KEY).property
        parts = json.loads(feature_line)
        pos = -1
        for item in parts:
            pos += 1
            if str(item.get('type')) == "link":
                a += process_link(pos, item)
    except Exception as e:
        a += "<h3>An error was thrown resulting in the incapability to display this footer:</h3>" + str(e)
    a += "<br /><center>Copyright (c) 2017 Doralitze</center></footer></body></html>"
    return a
