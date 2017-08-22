from django.http import HttpRequest


def render_headbar(httprequest, title="c3foc - admin"):
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


def render_footer(httprequest):
    return "</body></html>"