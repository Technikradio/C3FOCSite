from django.http import HttpRequest
from ..models import Media, Profile, GroupReservation
from .magic import get_current_user


def render_media_list(request: HttpRequest, u: Profile):
    m = GroupReservation.objects.all()
    if u.rights < 1:
        m.filter(createdByUser=u)
    a = "<table><tr><th> Preview </th><tr> Headline </tr></tr>"
    for r in m:
        a += "<tr>"

        a += "</tr>"
    a += "</table>"
    return a


def render_media_page(request: HttpRequest):
    a = '<span class="button"><a href="/admin/media/add">Upload Media</a></span>'
    u: Profile = get_current_user(request)
    a += render_media_list(request, u)
    return a
