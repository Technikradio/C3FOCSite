from .navbar import render_nav_bar
from ..management import magic
from ..models import Profile
# from .searching import render_search_bar


def render_content_header(http_request, title="C3FOC", admin_popup=False):
    # only while rendering isn't a thing
    a = '<html lang="en-US"><head>'
    a += '''<meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="/staticfiles/frontpage/w3.css" />
            <link rel="stylesheet" href="/staticfiles/frontpage/w3-theme-black.css" />
            <link rel="stylesheet" href="/staticfiles/frontpage/roboto.ttf" />
            <link rel="stylesheet" href="/staticfiles/frontpage/style.css">
            '''
    a += '<meta charset="UTF-8"><title>' + title + '</title></head>'
    a += '<body><header class="header">'
    if not admin_popup:
        a += render_nav_bar(http_request)
        # a += render_search_bar()
    else:
        a += '<div class="w3-bar w3-theme w3-top w3-left-align w3-large">'
        a += title
        a += ' | <a href="/admin">Back to dashboard</a><span class="user-menu">'
        p: Profile = magic.get_current_user(http_request)
        if not p is None:
            a += 'Logged in as ' + p.displayName + ' | '
            a += '<a href="/logout"> logout </a>'
        else:
            a += 'Not logged in'
        a += '</span>'
        a += '</div>'
    a += '</header>'
    a += '<div class="w3-main w3-padding-64">'
    return a
