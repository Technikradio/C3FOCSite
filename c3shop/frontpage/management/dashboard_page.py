from .page_skeleton import render_footer, render_headbar
from .order_page import render_open_order_table
from ..models import GroupReservation
from django.http import HttpRequest


def render_features_bar():
    a = '<div class="featurebar">'
    a += '<a href="/admin">Dashboard</a><br />'
    a += '<a href="/admin/posts">Posts</a><br />'
    a += '<a href="/admin/users">Users</a><br />'
    a += 'Articles<br />'
    a += 'Media<br />'
    a += '<a href="/admin/orders">reservations</a><br />'
    a += 'Global settings<br />'
    a += '<br/><a href="/logout/"> Logout </a><br/>'
    a += '</div>'
    return a


def render_statistics_panel(request: HttpRequest):
    a = '<div class="statistics">'
    # TODO implement order and other statistics here
    # Use user access level in order to determine which info is allowed to be rendered
    open_res: int = GroupReservation.objects.get(open=True).count()
    if open_res == 0:
        a += "There are 0 open reservations! YAY!<br />"
    else:
        non_done_res = GroupReservation.objects.get(open=True).filter(ready=False).count()
        a += "There are " + str(open_res) + " open reservations of which " + str(non_done_res) + \
             " still require some work.<br />"
    a += '</div>'
    return a


def render_order_panel():
    a = '<div class="open_orders">'
    a += render_open_order_table()
    a += '</div>'
    return a


def render_dashboard(request: HttpRequest):
    a = render_headbar(request)
    a += render_features_bar()
    a += '<div class="panel_board">'
    a += render_statistics_panel(request)
    a += render_order_panel()
    a += '</div>'
    a += render_footer(request)
    return a
