from .page_skeleton import render_footer, render_headbar
from django.http import HttpRequest


def render_features_bar():
    a = '<div class="featurebar">'
    a += '<a href="/admin/posts">Posts</a><br />'
    a += '<a href="/admin/users">Users</a><br />'
    a += 'Articles<br />'
    a += 'Media<br />'
    a += 'reservations<br />'
    a += 'Global settings<br />'
    a += '</div>'
    return a


def render_statistics_panel(request: HttpRequest):
    a = '<div class="statistics">'
    # TODO implement order and other statistics here
    # Use user access level in order to determine which info is allowed to be rendered
    a += '</div>'
    return a


def render_dashboard(request: HttpRequest):
    a = render_headbar(request)
    a += render_features_bar()
    a += render_statistics_panel(request)
    a += render_footer(request)
    return a
