from .navbar import render_nav_bar


def render_header(http_request, title="C3FOC", admin=False):
    # only while rendering isn't a thing
    if not admin:
        return '<html lang="en-US"><head><link rel="stylesheet" href="/staticfiles/frontpage/style.css">' \
               '<meta charset="UTF-8"><title>' + title + '</title></head>' \
               '<body><header class="header"><h1>C3FOC site</h1>' + render_nav_bar(http_request) + '</header>'
    else:
        # return the same for now
        return '<html lang="en-US"><head><link rel="stylesheet" href="/staticfiles/frontpage/style.css">' \
               '<meta charset="UTF-8"><title>' + title + '</title></head>' \
               '<body><header class="header"><h1>C3FOC site</h1>' + render_nav_bar(http_request) + '</header>'
