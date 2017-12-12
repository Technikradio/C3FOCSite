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


def render_confirm_popup(request: HttpRequest):
    back: str = request.GET.get("back_url")
    forward: str = request.GET.get("forward_url")
    payload: str = request.GET.get("payload")
    if not back:
        back = "/admin"
    if not forward:
        return "<h3>Something went wrong...</h3>There was an action requested but no forward url defined.<br/><br/>" + \
               '<br/><a href="/admin/" class="button">Go back to Dashboard</a>'
    if payload:
        payload = "?payload=" + payload
    else:
        payload = ""
    a = '<div class="w3-row w3-padding-64 w3-twothird w3-container">'
    a += "<h3>The action you've requested may be a bit destructive...</h3>"
    a += "Do you really want to do this?<br/><br/>"
    a += '<a href="' + back + '" class="button">Go back</a> <a href="' + forward + payload
    a += '" class="button">Continue</a></div>'
    return a
