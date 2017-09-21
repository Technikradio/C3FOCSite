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
        <meta charset="UTF-8">
        <title>%title%</title>
    </head>
    <body>
    """
    a = a.replace("%title%", title)
    return a


def render_footer(httprequest: HttpRequest):
    return "</body></html>"