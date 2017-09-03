from django.contrib import auth
from . import headerfunctions, footerfunctions
from django.http import HttpResponse, HttpResponseRedirect


def redirect(url):
    """
    This method redirects a user to the given url
    :param url: The URL to redirect to
    :return: The HTTP_Response
    """
    return HttpResponseRedirect(url)


def render_login_form(request, was_password_wrong):
    a = '<div class="login-form"><h2>Login</h2><form method="post" action="' + request.path + '" name="login-form">'
    if was_password_wrong:
        a += 'Your login credentials were incorrect.<br />'
    a += 'Username: <input type="text" name="username" /><br />'
    a += 'Password: <input type="password" name="password" /><br />'
    a += '<input type="submit" value="Login" /></form></div>'
    return a


def login(request, default_redirect="/"):
    """
    This method shows a login form if no POST credentials are given or will redirect the
    user after a success full login.
    :param request: The current HTTP request
    :param default_redirect: The URL to redirect to if no GET request is given
    :return: The correct HTTP_RESPONSE
    """
    forward = default_redirect
    if request.GET.get("next"):
        forward = request.GET["next"]
    wrong = False
    if request.POST.get("username") and request.POST.get("password"):
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            # User successfully authenticated himself. Log him in
            auth.login(request, user)
            return redirect(forward)
        else:
            wrong = True
            # Wrong credentials. Show login message again and an error message.
    a = headerfunctions.render_header(request, admin=True, title="C3FOC - Login")
    a += render_login_form(request, wrong)
    a += footerfunctions.render_footer(request)
    return HttpResponse(a)


def logout(request, default_redirect="/"):
    """
    This function logs a user out and redirect him to a certain location
    :param request: the current HTTP request
    :param default_redirect: The location to redirect if no next GET request is given
    :return: The HTTP_RESPONSE containing the redirect
    """
    auth.logout(request)
    forward = default_redirect
    if request.GET.get("next"):
        forward = request.GET["next"]
    return redirect(forward)


# TODO write registration utility for admins
