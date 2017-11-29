from .navbar import render_nav_bar
from .searching import render_search_bar


def render_content_header(http_request, title="C3FOC", admin_popup=False):
    # only while rendering isn't a thing
    a = '<html lang="en-US"><head>'
    a += '''<meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="/staticfiles/frontpage/w3.css" />
            <link rel="stylesheet" href="/staticfiles/frontpage/w3-theme-black.css" />
            <link rel="stylesheet" href="/staticfiles/frontpage/roboto.woff" />
            <!--<link rel="stylesheet" href="/staticfiles/frontpage/style.css">-->
            '''
    a += '<meta charset="UTF-8"><title>' + title + '</title></head>'
    a += '<body><header class="header">'
    if not admin_popup:
        a += '<h1>C3FOC site</h1>'
        a += render_nav_bar(http_request)
        a += render_search_bar()
    else:
        a += title
        a += ' | <a href="/admin">Back to dashboard</a><span class="user-menu">'
        a += '<a href="/logout"> logout </a>'
        a += '</span>'
    a += '</header>'
    return a
