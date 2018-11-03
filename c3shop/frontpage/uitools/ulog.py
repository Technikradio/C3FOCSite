from django.contrib import auth
from . import headerfunctions, footerfunctions
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from . import dataforge
import logging

logger = logging.getLogger(__name__)

def redirect(url):
    """
    This method redirects a user to the given url
    :param url: The URL to redirect to
    :return: The HTTP_Response
    """
    return HttpResponseRedirect(url)


def get_ip(request: HttpRequest):
    x_forward = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward:
        return x_forward.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')


def render_login_form(request: HttpRequest, was_password_wrong):
    forward = ""
    if request.GET.get("next"):
        forward = '?next=' + request.GET["next"]
    a = '<div class="login-form"><h2>Login</h2><form method="post" action="' + request.path + forward + \
        '" name="login-form">'
    a += dataforge.get_csrf_form_element(request)
    if was_password_wrong:
        a += 'Your login credentials were incorrect.<br />'
    a += 'Username: <input type="text" name="username" /><br />'
    a += 'Password: <input type="password" name="password" /><br />'
    a += '<input type="submit" value="Login" /></form></div>'
    return a


def login(request: HttpRequest, default_redirect="/"):
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
    logger.debug("Starting authentication (forward: " + forward)
    if request.POST.get("username") and request.POST.get("password"):
        try:
            username = request.POST["username"]
            password = request.POST["password"]
            logger.debug("Retrieved credentials trying to login. Remote: " + get_ip(request) + " Please wait...")
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                # User successfully authenticated himself. Log him in
                auth.login(request, user)
                logger.info("Successfully logged user '" + user.username + "' in...")
                return redirect(forward)
            else:
                wrong = True
                logger.debug("wrong credentials, displaying again")
        except Exception as e:
            logging.warning(str(e))
            wrong = True
    logger.debug("There was no correct credential transmit yet")
    a = headerfunctions.render_content_header(request, admin_popup=True, title="C3FOC - Login")
    a += render_login_form(request, wrong)
    a += footerfunctions.render_footer(request)
    return HttpResponse(a)


def logout(request: HttpRequest, default_redirect="/"):
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
    logger.info("User " + get_ip(request) + " logged out.")
    return redirect(forward)

