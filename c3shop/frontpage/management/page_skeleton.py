from django.http import HttpRequest

"""
The difference between this skeleton and the uitools.* header and footer is that this is used to display a minimalistic
menu like page.
"""


def render_headbar(httprequest: HttpRequest, title="c3foc - admin"):
    a = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link rel="stylesheet" href="/staticfiles/frontpage/style.css" />
        <link rel="stylesheet" href="/staticfiles/frontpage/w3.css" />
        <link rel="stylesheet" href="/staticfiles/frontpage/w3-theme-black.css" />
        <link rel="stylesheet" href="/staticfiles/frontpage/roboto.ttf" />
        <meta charset="UTF-8" />
        <title>%title%</title>
    </head>
    <body>
    """
    a = a.replace("%title%", title)
    a += '<header><div class="w3-bar w3-theme w3-top w3-left-align w3-large w3-padding-16">' \
         '<span class="w3-padding-16">Administration & Statistics</span></div></header>'
    return a


def render_footer(httprequest: HttpRequest):
    return "</body></html>"
