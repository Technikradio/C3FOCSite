from django.http import HttpRequest
from ..models import Media, Profile
from .magic import get_current_user


def render_media_list(request: HttpRequest, u: Profile):
    m = Media.objects.all()
    if u.rights < 1:
        #Maybe implement filtering on own media
        pass
    a = "<table><tr><th> Preview </th><tr> Headline </tr></tr>"
    for r in m:
        a += "<tr>"
        a += '<td><img class="icon" src="' + str(r.lowResFile) + '" /></td>'
        a += '<td>' + str(r.headline) + '</td>'
        a += "</tr>"
    a += "</table>"
    return a


def render_media_page(request: HttpRequest):
    a = '<br /><br /><span class="button"><a href="/admin/media/add">Upload Media</a></span><br /><br />'
    u: Profile = get_current_user(request)
    a += render_media_list(request, u)
    return a
