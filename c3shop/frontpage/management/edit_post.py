from django.http import HttpRequest

from . import page_skeleton
from .form import Form, TextField, PlainText, TextArea, SubmitButton
from ..models import Post


def render_edit_page(http_request: HttpRequest, action_url: str):
    post_id = None
    post = None
    if http_request.GET.get("post_id"):
        post_id = int(http_request.GET["post_id"])
    if post_id is not None:
        post = Post.objects.get(pk=post_id)
    f = Form()
    f.action_url = action_url
    f.add_content(PlainText("Post title:"))
    if post is None:
        f.add_content(TextField(name="title"))
        f.add_content(TextArea(name="post_text", label_text="Post content (as MarkDown)",
                               placeholder="Write the post as markdown here"))
    else:
        f.add_content(TextField(button_text=post.title, name="title"))
        f.add_content(TextArea(name="post_text", label_text="Post content (as MarkDown)", text=post.text,
                               placeholder="Write the post as markdown here"))
    f.add_content(SubmitButton())
    a = page_skeleton.render_headbar(http_request, "Edit Post")
    a += f.render_html()
    a += page_skeleton.render_footer(http_request)
    return a
