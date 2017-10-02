from .navbar import render_nav_bar


def render_content_header(http_request, title="C3FOC", admin_popup=False):
    # only while rendering isn't a thing
    a = '<html lang="en-US"><head>'
    a += '<link rel="stylesheet" href="/staticfiles/frontpage/style.css">'
    a += '<meta charset="UTF-8"><title>' + title + '</title></head>'
    a += '<body><header class="header">'
    if not admin_popup:
        a += '<h1>C3FOC site</h1>'
        a += render_nav_bar(http_request)
    else:
        a += "Edit post"
    a += '</header>'
    return a
