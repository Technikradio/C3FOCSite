from .page_skeleton import render_footer, render_headbar
from .reservation_page import render_open_order_table
from ..models import GroupReservation, Profile, Settings, Article
from . import magic
from django.http import HttpRequest


def render_features_bar():
    a = '<div class="w3-third w3-container w3-padding-64">'
    a += '<a href="/admin">Dashboard</a><br />'
    a += '<a href="/admin/posts">Posts</a><br />'
    a += '<a href="/admin/users">Users</a><br />'
    a += '<a href="/admin/articles">Articles</a><br />'
    a += '<a href="/admin/media">Media</a><br />'
    a += '<a href="/admin/reservations">Reservations</a><br />'
    a += 'Global settings<br />'
    a += '<br/><a href="/logout/"> Logout </a><br/>'
    a += '</div>'
    return a


def render_statistics_panel(request: HttpRequest):
    a = '<div class="w3-row w3-padding-64 w3-twothird w3-container">'
    a += '<h3 class="w3-text-teal">Statistics</h3>'
    # TODO implement order and other statistics here
    # Use user access level in order to determine which info is allowed to be rendered
    open_res: int = GroupReservation.objects.filter(open=True).count()
    if open_res == 0:
        a += "There are 0 open reservations! YAY!<br />"
    else:
        non_done_res = GroupReservation.objects.filter(open=True).filter(ready=False).count()
        a += "There are " + str(open_res) + " open reservations of which " + str(non_done_res) + \
             " still require some work.<br /><br />"
    a += '</div>'
    return a


def render_order_panel(u: Profile):
    a = '<div class="w3-row w3-padding-64 w3-twothird w3-container">'
    a += '<h3 class="w3-text-teal">Open orders</h3>'
    a += render_open_order_table(u)
    a += '</div>'
    return a


def render_quick_store_panel():
    a = '<div class="w3-row w3-padding-64 w3-twothird w3-container">'
    a += '<h3 class="w3-text-teal">Store status</h3>'
    if magic.parse_bool(Settings.objects.get(SName="frontpage.store.open").property.lower()):
        a += "The store is currently open<br/>"
    else:
        a += "The store is currently closed<br/>"
    a += '<br/><a href="/admin/actions/change-open-status" class="button">Toggle open status</a><br /><br />'
    a += '</div>'
    return a


def render_quick_article_panel():
    a = '<div class="w3-row w3-padding-64 w3-twothird w3-container">'
    a += '<h3 class="w3-text-teal">QAP</h3>'
    try:
        s: Settings = Settings.objects.get(SName="frontpage.chestsize")
        size: int = int(s.property)
        a += "<br />Quick decrease:<br />"
        a += '<table><tr><th>Article</th><th>Quantity</th><th>Lower by ' + str(size) + ' Items</th></tr>'
        for article in Article.objects.exclude(quantity=0).order_by('quantity'):
            a += '<tr><td>' + article.description + '</td><td>' + str(article.quantity) + '</td>'
            a += '<td><a href="/admin/actions/reduce?article_id=' + str(article.pk) + '" class="button">'
            a += 'Reduce amount</a></td></tr>'
        a += '</table>'
    except Exception as e:
        a += "Error: " + str(e)
    a += '</div>'
    return a


def render_error_panel(request: HttpRequest):
    if request.GET.get("error"):
        return '<div class="error-panel">Something produced an error: ' + request.GET["error"] + '</div>'
    else:
        return ""


def render_dashboard(request: HttpRequest):
    u: Profile = magic.get_current_user(request)
    a = render_headbar(request)
    #a += render_features_bar()
    a += render_error_panel(request)
    #a += '<div>'
    a += render_statistics_panel(request)
    a += render_features_bar()
    a += render_quick_article_panel()
    a += render_order_panel(u)
    if u.rights > 1:
        a += render_quick_store_panel()
    #a += '</div>'
    a += render_footer(request)
    return a
