from django.http import HttpRequest, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth.models import User
from . import page_skeleton, magic
from .form import Form, TextField, PlainText, TextArea, SubmitButton, NumberField, PasswordField
from ..models import Profile


def render_edit_page(http_request: HttpRequest, action_url: str):

    user_id = None
    profile: Profile = None
    if http_request.GET.get("user_id"):
        user_id = int(http_request.GET["user_id"])
    if user_id is not None:
        profile = Profile.objects.get(pk=user_id)
    f = Form()
    f.action_url = action_url
    if profile:
        f.add_content(PlainText('Edit user "' + profile.authuser.username + '"'))
    else:
        f.add_content(PlainText('Add new user'))
    if not profile:
        f.add_content(PlainText("username (can't be edited later on): "))
        f.add_content(TextField(name='username'))
    # TODO implement to display active field only when current user is admin
    f.add_content(PlainText('Display name: '))
    if profile:
        f.add_content(PlainText("Email address: "))
        f.add_content(TextField(name='email', text=str(profile.authuser.email)))
        f.add_content(TextField(name='display_name', button_text=profile.displayName))
        f.add_content(PlainText('DECT: '))
        f.add_content(NumberField(name='dect', button_text=str(profile.dect)))
        f.add_content(PlainText('Notes:<br/>'))
        f.add_content(TextArea(name='notes', text=str(profile.notes)))
    else:
        f.add_content(PlainText("Email address: "))
        f.add_content(TextField(name='email'))
        f.add_content(TextField(name='display_name'))
        f.add_content(PlainText('DECT: '))
        f.add_content(NumberField(name='dect'))
        f.add_content(PlainText('Notes:<br/>'))
        f.add_content(TextArea(name='notes', placeholder="Hier könnte ihre Werbung stehen"))
    if profile:
        f.add_content(PlainText('<br/>Change password (leave blank in order to not change it):'))
    else:
        f.add_content(PlainText('<br/>Choose a password: '))
    f.add_content(PasswordField(name='password'))
    f.add_content(PlainText('Confirm your password: '))
    f.add_content(PasswordField(name='confirm_password'))
    f.add_content(SubmitButton())
    a = page_skeleton.render_headbar(http_request, "Edit User")
    a += f.render_html()
    a += page_skeleton.render_footer(http_request)
    return a


def check_password_conformity(pw1: str, pw2: str):
    if not pw1 == pw2:
        return False
    if len(pw1) < 6:
        return False
    if pw1.isupper():
        return False
    if pw1.islower():
        return False
    return True


def action_save_user(request: HttpRequest, default_forward_url: str = "/admin/users"):
    """
    This functions saves the changes to the user or adds a new one. It completely creates the HttpResponse
    :param request: the HttpRequest
    :param default_forward_url: The URL to forward to if nothing was specified
    :return: The crafted HttpResponse
    """
    forward_url = default_forward_url
    if request.GET.get("redirect"):
        forward_url = request.GET["redirect"]
    if not request.user.is_authentificated():
        return HttpResponseForbidden()
    profile = Profile.objects.get(authuser=request.user)
    if profile.rights < 2:
        return HttpResponseForbidden()
    try:
        if request.GET.get("user_id"):
            pid = int(request.GET["user_id"])
            displayname = str(request.GET["display_name"])
            dect = int(request.GET["dect"])
            notes = str(request.GET["notes"])
            pw1 = str(request.GET["password"])
            pw2 = str(request.GET["confirm_password"])
            mail = str(request.GET["email"])
            user: Profile = Profile.objects.get(pk=pid)
            user.displayName = displayname
            user.dect = dect
            user.notes = notes
            if check_password_conformity(pw1, pw2):
                au: User = user.authuser
                # TODO change password
                au.save()
            user.save()
        else:
            # assume new user
            username = str(request.GET["username"])
            displayname = str(request.GET["display_name"])
            dect = int(request.GET["dect"])
            notes = str(request.GET["notes"])
            pw1 = str(request.GET["password"])
            pw2 = str(request.GET["confirm_password"])
            mail = str(request.GET["email"])
            # TODO create auth_user
            pass
        pass
    except Exception as e:
        return HttpResponseBadRequest(str(e))
    return redirect(forward_url)
