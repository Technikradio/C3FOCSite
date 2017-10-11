from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponseBadRequest
from ..models import Profile, Media


def action_change_user_avatar(request: HttpRequest):
    try:
        user_id = request.GET["payload"]
        media_id = request.GET["media_id"]
        user: Profile = Profile.objects.get(pk=int(user_id))
        medium = Media.objects.get(pk=int(media_id))
        user.avatarMedia = medium
        user.save()
    except Exception as e:
        return HttpResponseBadRequest(e)
    return redirect("/admin/users")
