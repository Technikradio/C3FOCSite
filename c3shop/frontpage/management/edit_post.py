import logging
from django.http import HttpRequest, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import redirect
from . import magic
from .form import Form, TextField, PlainText, TextArea, SubmitButton, NumberField
from ..models import Post, Profile
from ..uitools.dataforge import get_csrf_form_element


def render_edit_page(http_request: HttpRequest, action_url: str):
    """
    This function renders a page to edit a post. It checks the GET segment for a 'post_id' field and loads that post.
    :param http_request: The http request
    :param action_url: The action URL (at least containing the 'post_id' field and should contain a 'redirect' field.
    :return: The rendered HTML code
    """
    post_id = None
    post = None
    if http_request.GET.get("post_id"):
        post_id = int(http_request.GET["post_id"])
    if post_id is not None:
        post = Post.objects.get(pk=post_id)
    f = Form()
    f.action_url = action_url
    f.add_content(PlainText('<br />'))
    if not post:
        f.add_content(PlainText('Add new Post: <br />'))
    f.add_content(PlainText("Post title:"))
    if post is None:
        f.add_content(TextField(name="title"))
        f.add_content(TextArea(name="post_text", label_text="<br/>Post content (as MarkDown):",
                               placeholder="Write the post as markdown here"))
        f.add_content(PlainText('<br />'))
        f.add_content(PlainText("Required user permission: "))
        number_field = NumberField(name="required_permission")
        number_field.minimum = -1
        number_field.maximum = 4
        number_field.button_text = -1
        f.add_content(number_field)
    else:
        f.add_content(TextField(button_text=post.title, name="title"))
        f.add_content(TextArea(name="post_text", label_text="Post content (as MarkDown)", text=post.text,
                               placeholder="Write the post as markdown here"))
        f.add_content(PlainText('<br />'))
        f.add_content(PlainText("Required user permission: "))
        number_field = NumberField(name="required_permission")
        number_field.minimum = -1
        number_field.maximum = 4
        number_field.button_text = post.visibleLevel
        f.add_content(number_field)
    f.add_content(PlainText(get_csrf_form_element(http_request)))
    f.add_content(SubmitButton())
    # a = page_skeleton.render_headbar(http_request, "Edit Post")
    a = f.render_html()
    # print(f.render_html())
    # a += page_skeleton.render_footer(http_request)
    return a


def do_edit_action(request: HttpRequest, default_forward_url: str = ".."):
    """
    This function handles an post edit request. The user must be logged in and allowed to edit posts. NOTE that this
    function returns a completely done HTTPResponse. No further crafting required.
    :param request: The http request
    :param default_forward_url: A URL to forward to if no 'redirect' field is given in the GET section
    :return: The crafted HTTPResponse
    """
    forward_url = default_forward_url
    if request.GET.get("redirect"):
        forward_url = request.GET["redirect"]
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    profile = Profile.objects.get(authuser=request.user)
    if profile.rights < 2:
        return HttpResponseForbidden()
    # Now we checked that the user is permitted and continue with the modification
    mpost = None
    if not request.GET.get("post_id"):
        # Assuming a new Post
        mpost = Post()
        mpost.createdByUser = profile
        logging.log(logging.INFO, "User '" + str(profile) + "' is creating a new post")
    else:
        # We have a desired post id. Let's load that one
        ids: str = request.GET["post_id"]
        mpost = Post.objects.get(pk=int(ids))
        logging.log(logging.INFO, "Editing post [" + str(ids) + "] containing: " + str(mpost))
    if request.POST.get('title'):
        mpost.title = str(request.POST['title'])
    else:
        return HttpResponseBadRequest()
    if request.POST.get('post_text'):
        mpost.text = str(request.POST.get('post_text'))
        mpost.cacheText = magic.compile_markdown(mpost.text)
    else:
        return HttpResponseBadRequest()
    if request.POST.get('required_permission'):
        mpost.visibleLevel = int(request.POST["required_permission"])
    else:
        return HttpResponseBadRequest()
    mpost.save()
    return redirect(forward_url)


def do_delete_action(request: HttpRequest):
    if not request.GET.get("payload"):
        return redirect("/admin?error=NO_POST_ID_TO_DELETE")
    id: int = int(request.GET["payload"])
    Post.objects.get(pk=id).delete()
    return redirect("/admin/posts")
