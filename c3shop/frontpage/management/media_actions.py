from datetime import date, time
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponseBadRequest
from ..models import Profile, Media, MediaUpload
from .magic import compile_markdown, get_current_user

import logging


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


def handle_file(u: Profile, headline: str, category: str, text: str, file):
    m: Media = Media()
    high_res_file_name = 'uploads/' + str(date.today().year) + '/HIGHRES_' + file.name.replace(" ", "_")
    low_res_file_name = 'uploads/' + str(date.today().year) + '/LOWRES_' + file.name.replace(" ", "_")
    with open(high_res_file_name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    # TODO crop image
    m.text = text
    m.cachedText = compile_markdown(text)
    m.category = category
    m.highResFile = high_res_file_name
    m.lowResFile = low_res_file_name
    m.headline = headline
    m.save()
    mu: MediaUpload = MediaUpload()
    mu.UID = u
    mu.MID = m
    mu.save()
    logging.info("Uploaded file '" + file.name + "' and cropped it. The resulting PK is " + m.pk)


def action_add_single_media(request: HttpRequest):
    try:
        headline = request.POST["headline"]
        category = request.POST["category"]
        text = request.POST["text"]
        file = request.FILES['file']
        user: Profile = get_current_user(request)
        handle_file(user, headline, category, text, file)
    except Exception as e:
        return redirect("/admin/media/add?hint=" + str(e))
    return redirect("/admin/media/add")


def action_add_multiple_media(request: HttpRequest):
    try:
        category: str = request.POST["category"]
        files = request.FILES.getlist('file_field')
        user: Profile = get_current_user(request)
        for f in files:
            handle_file(user, str(f.name), category, "### There is no media description", f)
    except Exception as e:
        return redirect("/admin/media/add?hint=" + str(e))
    return redirect("/admin/media/add")
