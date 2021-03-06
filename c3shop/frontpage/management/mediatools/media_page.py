from django.http import HttpRequest
from frontpage.models import Media, Profile
from frontpage.models import MediaUpload
from frontpage.management.magic import get_current_user


def render_media_list(request: HttpRequest, u: Profile):
    m = Media.objects.all()
    if u.rights < 1:
        # Maybe implement filtering on own media
        pass
    a = "<table><tr><th> Preview </th><th> Headline </th><th> Uploaded by User</th></tr>"
    for r in m:
        mu: MediaUpload = MediaUpload.objects.get(MID=r)
        a += "<tr>"
        a += '<td><img class="icon" src="' + str(r.lowResFile) + '" /></td>'
        a += '<td>' + str(r.headline) + '</td><td>' + mu.UID.displayName + '</td>'
        a += "</tr>"
    a += "</table>"
    return a


def render_media_page(request: HttpRequest):
    a = '<div class="admin-popup w3-row w3-padding-64 w3-twothird w3-container"><br /><br />' \
            '<a href="/admin/media/add" class="button">Upload Media</a><br /><br />'
    u: Profile = get_current_user(request)
    a += render_media_list(request, u)
    a += "</div>"
    return a
