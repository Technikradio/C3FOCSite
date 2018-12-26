from datetime import date, time
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponseBadRequest
from ..models import Profile, Media, MediaUpload
from .magic import compile_markdown, get_current_user

import logging
import os
import math
import PIL
from PIL import Image


PATH_TO_UPLOAD_FOLDER_ON_DISK: str = "/usr/local/www/focweb/uploads/"
IMAGE_SCALE = 64

def action_change_user_avatar(request: HttpRequest):
    try:
        user_id = int(request.GET["payload"])
        media_id = int(request.GET["media_id"])
        user: Profile = Profile.objects.get(pk=int(user_id))
        u: Profile = get_current_user(request)
        if not (u == user) and u.rights < 4:
            return redirect("/admin?error='You're not allowed to edit other users.'")
        medium = Media.objects.get(pk=int(media_id))
        user.avatarMedia = medium
        user.save()
    except Exception as e:
        return redirect("/admin?error=" + str(e))
    return redirect("/admin/users")


def handle_file(u: Profile, headline: str, category: str, text: str, file):
    m: Media = Media()
    upload_base_path: str = 'uploads/' + str(date.today().year)
    high_res_file_name = upload_base_path + '/HIGHRES_' + file.name.replace(" ", "_")
    low_res_file_name = upload_base_path + '/LOWRES_' + file.name.replace(" ", "_")
    if not os.path.exists(PATH_TO_UPLOAD_FOLDER_ON_DISK + upload_base_path):
        os.makedirs(PATH_TO_UPLOAD_FOLDER_ON_DISK + upload_base_path)
    with open(high_res_file_name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    # TODO crop image
    original = Image.open(high_res_file_name)
    width, height = original.size
    diameter = math.sqrt(math.pow(width, 2) + math.pow(height, 2))
    width /= diameter
    height /= diameter
    width *= IMAGE_SCALE
    height *= IMAGE_SCALE
    cropped = original.resize((int(width), int(height)), PIL.Image.LANCZOS)
    cropped.save(low_res_file_name)
    m.text = text
    m.cachedText = compile_markdown(text)
    m.category = category
    m.highResFile = "/" + high_res_file_name
    m.lowResFile = "/" + low_res_file_name
    m.headline = headline
    m.save()
    mu: MediaUpload = MediaUpload()
    mu.UID = u
    mu.MID = m
    mu.save()
    logging.info("Uploaded file '" + str(file.name) + "' and cropped it. The resulting PK is " + str(m.pk))


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
        files = request.FILES.getlist('files')
        user: Profile = get_current_user(request)
        for f in files:
            handle_file(user, str(f.name), category, "### There is no media description", f)
    except Exception as e:
        return redirect("/admin/media/add?hint=" + str(e))
    return redirect("/admin/media/add")
