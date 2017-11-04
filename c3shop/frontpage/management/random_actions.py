from ..models import Settings
from django.http import HttpRequest
from django.shortcuts import redirect


def action_change_store_open_status(request: HttpRequest):
    redirect_url = "/admin/"
    if request.GET.get("redirect"):
        redirect_url = request.GET["redirect"]
    s: Settings = Settings.objects.get(SName="frontpage.store.open")
    toggle_to = not (s.property.lower() in ("yes", "true", "t", "1"))
    if request.GET.get("toggle_to"):
        toggle_to = request.GET["toggle_to"].lower() in ("yes", "true", "t", "1")
    s.property = str(toggle_to)
    s.save()
    return redirect(redirect_url)
