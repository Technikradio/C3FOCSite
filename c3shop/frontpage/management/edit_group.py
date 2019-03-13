from django.http import HttpRequest
from ..models import ArticleGroup, Article
from .form import Form, SubmitButton, TextField, PlainText, NumberField, Select


def get_article_dict(grp: ArticleGroup):
    arts = Article.objects.all().filter(group=grp)
    sizesdict = {}
    sizes = []
    types = []
    for article in arts:
        if article.size not in sizesdict:
            sizesdict[article.size] = {article.type : (article.quantity, article.price)}
            if article.size not in sizes:
                sizes.append(article.size)
            if article.type not in types:
                types.append(article.type)
        else:
            sizesdict[article.size][article.type] = (article.quantity, article.price)
            if article.type not in types:
                types.append(article.type)
    sizes.sort()
    types.sort()
    return (sizes, types, sizesdict)


def get_article_matrix_form(request: HttpRequest, grp: ArticleGroup):
    f: Form = Form()
    f.action_url = "/admin/actions/update-group-articles?gid=" + str(grp.id)
    sizes, types, sizesdict = get_article_dict(grp)
    f.add(PlainText('Add new size:'))
    f.add(TextField(name="newsize"))
    f.add(PlainText('Add new Type:'))
    f.add(Select(name="newtype", text="type", content=[(-1, "Do not add a new type"), (0, "Unisex"),
        (1, "Female"), (2, "Male"), (3, "Kids")]))
    f.add(PlainText("<br /><table><tr><th>Size</th>"))
    for t in types:
        f.add(PlainText("<th>" + str(t) + '</th>'))
    f.add(PlainText("</tr>"))
    for s in sizes:
        f.add(PlainText("<tr><td>" + str(s) + '</td>'))
        # No need to check for avaiabilility of s in dict since there needs
        # to be at least one type of that size
        for t in types:
            f.add(PlainText("<td>"))
            if sizesdict[s].get(t):
                quantity, price = sizesdict[s][t]
                f.add(PlainText("Price [ct]: "))
                f.add(NumberField(name="price_" + str(s) + '_' + str(t),
                    button_text=str(price), minimum=0))
                f.add(PlainText("Quantity: "))
                f.add(NumberField(name="quantity_" + str(s) + '_' + str(t),
                    button_text=str(quantity), minimum=0))
            else:
                f.add(PlainText('<a href="/admin/actions/add-article-to-group?gid=' + 
                    str(grp.id) + '&size=' + str(s) + '&type=' + str(t)
                    + '" class="button">Add Article</a>'))
            f.add(PlainText("</td>"))
        f.add(PlainText("</tr>"))
    f.add(PlainText("</table>"))
    f.add(SubmitButton(button_text="update"))
    return f.render_html(request)


def render_edit_page(request: HttpRequest):
    a = '<div class="admin-popup w3-twothird w3-padding-64 w3-row w3-container">'
    grp: ArticleGroup = None
    if request.GET.get("group"):
        try:
            grp = ArticleGroup.objects.get(id=int(request.GET.get("group")))
        except:
            return "We'd like to display something but someone (most likely you) tampered" \
                    " with the GET request."
    # TODO build release articles button (underConstruction -> false)
    f: Form = Form()
    f.action_url = "/admin/actions/alter-article-group"
    if grp:
        f.action_url += "?gid=" + str(grp.id)
    a += f.render_html(request)
    if grp:
        # We're editing a group an hence need to display the matrix
        a += get_article_matrix_form(request, grp)
    a += "</div>"
    return a
