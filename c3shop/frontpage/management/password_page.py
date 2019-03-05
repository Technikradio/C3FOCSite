from ..models import Profile
from django.http import HttpRequest
from django.shortcuts import redirect
from .magic import get_current_user
from .form import Form, PlainText, PasswordField, SubmitButton, FieldGroup
from .messages import get_message
from .edit_user import check_password_conformity

def render_password_change_panel(request: HttpRequest):
    a = ""
    if request.GET.get("msgid"):
        a = '<div class="error-panel w3-row w3-container">' + get_message(request.GET["msgid"]) + '</div>'
    a += '<div class="admin-popup w3-row w3-padding-64 w3-twothird w3-container">'
    f: Form = Form("/admin/actions/change-password?next=/admin")
    f.add_content(PlainText("Please keep the basic rules of creating good passwords in"\
            + " mind and please do not use a single password twice!<br />But first you " \
            + "need to retype your current password so we can make sure it's you.<br />"))
    f.add(PlainText("Type in your old password: "))
    f.add(PasswordField(name="oldpassword"))
    fg: FieldGroup = FieldGroup(text="Change Password:")
    fg.add(PlainText("Type new password: "))
    fg.add(PasswordField(name="newpassword"))
    fg.add(PlainText("Confirm password: "))
    fg.add(PasswordField(name="confirmpassword"))
    f.add_content(fg)
    f.add_content(SubmitButton())
    a += f.render_html(request)
    a += '</div>'
    return a


def action_change_password(request: HttpRequest):
    if ((not request.POST.get("oldpassword")) or (not request.POST.get("newpassword"))
            or (not request.POST.get("confirmpassword"))):
        return redirect("/admin?msgid=invalidrequest")
    p: Profile = get_current_user(request)
    pw = request.POST["newpassword"]
    pwck = request.POST["confirmpassword"]
    oldpw = request.POST["oldpassword"]
    if pw == oldpw:
        return redirect("/admin/changepassword?msgid=changepassword.oldisnew")
    if not pw == pwck:
        return redirect("/admin/changepassword?msgid=changepassword.mismatch")
    if not check_password_conformity(pw, pwck):
        return redirect("/admin/changepassword?msgid=changepassword.rulemismatch")
    if not p.authuser.check_password(oldpw):
        return redirect("/admin/changepassword?msgid=changepassword.oldmismatch")
    p.authuser.set_password(pw)
    p.authuser.save()
    p.mustChangePassword = False
    p.save()
    return redirect("/admin?success&msgid=changepassword.success")


