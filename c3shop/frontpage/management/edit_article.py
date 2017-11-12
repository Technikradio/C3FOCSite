from django.http import HttpRequest
from . import page_skeleton, magic
from .form import Form, TextField, PlainText, TextArea, SubmitButton, NumberField, CheckBox, CheckEnum, Select
from ..models import Article, ArticleMedia
from ..uitools.dataforge import get_csrf_form_element


def render_image_table(art: Article):
    imgs = ArticleMedia.objects.all().filter(AID=art)
    a = ''
    a += '<table><tr><th> Preview </th><th> Headline </th></tr>'
    for img in imgs:
        media = img.MID
        a += '<tr><td><img src="' + media.lowResFile + '" /></td><td>' + media.headline + '</td>'
        a += "</tr>"
    a += '</table></div>'
    return a


def render_edit_page(http_request: HttpRequest):
    article_id = None
    article: Article = None
    if http_request.GET.get("article_id"):
        article_id = int(http_request.GET["article_id"])
    if article_id is not None:
        article = Article.objects.get(pk=article_id)
    f = Form()
    f.action_url = "/admin/actions/save-article"
    if article_id is not None:
        f.action_url += "?id=" + str(article_id)
    if not article:
        # Assume new article
        f.add_content(PlainText("<h3>Add a new Article</h3>Short Description / Name: "))
        f.add_content(TextField(name="description"))
        f.add_content(CheckBox(text="Visible: ", name="visible", checked=CheckEnum.CHECKED))
        f.add_content(PlainText("Price: "))
        f.add_content(TextField(name="price", do_cr_after_input=False))
        f.add_content(PlainText(" €ct<br/>Number of articles left: "))
        f.add_content(NumberField(name="quantity", minimum=0))
        f.add_content(PlainText("Size: "))
        f.add_content(TextField(name="size"))
        f.add_content(Select(name="type", text="type", content=[(0, "Unisex"), (1, "Female"), (2, "Male"), (3, "Kids")]))
        # f.add_content(NumberField(button_text=0, name="type", minimum=0, maximum=3))
        f.add_content(TextArea(name="largetext", label_text="Description",
                               placeholder="Write the large description here"))
        f.add_content(PlainText("<br />"))
    else:
        f.add_content(PlainText("<h3>Edit article #" + str(article.pk) + "</h3>Short Description / Name: "))
        f.add_content(TextField(name="description", button_text=article.description))
        f.add_content(CheckBox(text="Visible: ", name="visible", checked=CheckEnum.get_state(article.visible)))
        f.add_content(PlainText("Price: "))
        f.add_content(TextField(name="price", do_cr_after_input=False, button_text=article.price))
        f.add_content(PlainText(" €ct<br/>Number of articles left: "))
        f.add_content(NumberField(name="quantity", minimum=0, button_text=article.quantity))
        f.add_content(PlainText("Size: "))
        f.add_content(TextField(name="size", button_text=article.size))
        f.add_content(Select(name="type", text="type", content=[(0, "Unisex"), (1, "Female"), (2, "Male"), (3, "Kids")],
                             preselected=article.type))
        f.add_content(TextArea(name="largetext", label_text="Description",
                               text=article.largeText))
        f.add_content(PlainText("<br />"))
    f.add_content(SubmitButton())
    a = '<div class="admin-popup">'
    a += f.render_html()
    a += "<br />"
    if article:
        a += render_image_table(article)
    else:
        a += '</div>'
    return a
