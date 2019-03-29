import operator

from django.http import HttpRequest
from frontpage.models import ArticleGroup, Article
from frontpage.management.form import Form, SubmitButton, TextField, PlainText, NumberField, Select, TextArea, FieldGroup, CheckBox
from frontpage.management.dashboard_page import render_error_panel
from frontpage.uitools.body import get_type_string

def get_article_dict(grp: ArticleGroup):
    arts = Article.objects.all().filter(group=grp)
    sizesdict = {}
    sizes = []
    types = []
    for article in arts:
        if article.size not in sizesdict:
            sizesdict[article.size] = {article.type : (article.quantity, article.price, article.id,
                article.description, article.visible)}
            if article.size not in sizes:
                sizes.append(article.size)
            if article.type not in types:
                types.append(article.type)
        else:
            sizesdict[article.size][article.type] = (article.quantity, article.price, article.id,
                    article.description, article.visible)
            if article.type not in types:
                types.append(article.type)
    sizes.sort()
    types.sort()
    return (sizes, types, sizesdict)


def get_default_description(grp: ArticleGroup):
    matches_des = {}
    matches_cs = {}
    matches_text = {}
    for a in Article.objects.all().filter(group=grp):
        if not matches_des.get(a.description):
            matches_des[a.description] = 0
        matches_des[a.description] += 1
        if not matches_cs.get(a.chestsize):
            matches_cs[a.chestsize] = 0
        matches_cs[a.chestsize] += 1
        if not matches_text.get(a.largeText):
            matches_text[a.largeText] = 0
        matches_text[a.largeText] += 1
    p = (max(matches_des.items(), key=operator.itemgetter(1))[0],
            max(matches_cs.items(), key=operator.itemgetter(1))[0],
            max(matches_text.items(), key=operator.itemgetter(1))[0])
    return p


def get_article_matrix_form(request: HttpRequest, grp: ArticleGroup, defprice=""):
    f: Form = Form()
    f.action_url = "/admin/actions/update-group-articles?gid=" + str(grp.id) + "&dp=" + defprice
    sizes, types, sizesdict = get_article_dict(grp)
    default_description = ""
    if len(sizes) == 0:
        f.add(PlainText("Default description: "))
        f.add(TextField(name="defaultdescription", button_text="disabled until you add your first article",
            enabled=False))
        f.add(TextArea(name="defaulttext", label_text="Default text:",
            text="Disabled until you add the first article", enabled=False))
        f.add(PlainText("Default chest size: "))
        f.add(NumberField(name="defaultchestsize", button_text="25"))
    else:
        default_description, default_cs, default_text = get_default_description(grp)
        f.add(PlainText("Default description: "))
        f.add(TextField(name="defaultdescription", button_text=default_description))
        f.add(TextArea(name="defaulttext", label_text="Default text:",
            text=default_text))
        f.add(PlainText("Default chest size: "))
        f.add(NumberField(name="defaultchestsize", button_text=str(default_cs)))
        f.add(CheckBox(name="forceupdate", text="Force an update of the defaults"))
    fg: FieldGroup = FieldGroup(text="Add a new Section")
    fg.add(PlainText('(Please fill in both)<br />Add new size: '))
    fg.add(TextField(name="newsize"))
    fg.add(PlainText('Add new Type: '))
    fg.add(Select(name="newtype", text="", content=[(0, "Unisex"),
        (1, "Female"), (2, "Male"), (3, "Kids"), (-1, "Do not add a new type")], preselected=4))
    f.add(fg)
    f.add(SubmitButton(button_text="update"))
    f.add(PlainText("<br /><table><tr><th>Size</th>"))
    for t in types:
        f.add(PlainText("<th>" + get_type_string(t) + '</th>'))
    f.add(PlainText("</tr>"))
    for s in sizes:
        f.add(PlainText("<tr><td>" + str(s) + '</td>'))
        # No need to check for avaiabilility of s in dict since there needs
        # to be at least one type of that size
        for t in types:
            f.add(PlainText("<td>"))
            if sizesdict[s].get(t):
                quantity, price, aid, description, v = sizesdict[s][t]
                if description != default_description:
                    f.add(PlainText('<img src="/staticfiles/frontpage/warning.png" class="icon" /> Different desctiption'))
                    f.add(PlainText(': <br /><br /><details><summary class="button">Show</summary><br /><br />' \
                            + description + '</details><br />'))
                f.add(PlainText('<a href="/admin/articles/edit?article_id=' + str(aid)
                    + '"><img src="/staticfiles/frontpage/edit.png" class="button-img"/></a>'))
                if not v:
                    f.add(PlainText('<img class="icon" src="/staticfiles/frontpage/ghost.png" />'))
                f.add(PlainText("<br />Price [ct]: "))
                f.add(NumberField(name="price_" + str(s) + '_' + str(t),
                    button_text=str(price), minimum=0))
                f.add(PlainText("Quantity: "))
                f.add(NumberField(name="quantity_" + str(s) + '_' + str(t),
                    button_text=str(quantity), minimum=0))
            else:
                f.add(PlainText('<a href="/admin/actions/add-article-to-group?gid=' + 
                    str(grp.id) + '&size=' + str(s) + '&type=' + str(t) + "&dp=" + defprice
                    + '" class="button">Add Article</a>'))
            f.add(PlainText("</td>"))
        f.add(PlainText("</tr>"))
    f.add(PlainText('</table><br />'))
    f.add(SubmitButton(button_text="update", do_cr_after_input=False))
    f.add(PlainText('<a href="/admin/actions/release-group?gid=' + \
            str(grp.id) + '&dp=' + defprice + '" class="button">Release Group</a>'))
    return f.render_html(request)


def render_edit_page(request: HttpRequest):
    a = '<div class="admin-popup w3-twothird w3-padding-64 w3-row w3-container">'
    grp: ArticleGroup = None
    dp = "0"
    if request.GET.get("gid"):
        try:
            grp = ArticleGroup.objects.get(id=int(request.GET.get("gid")))
        except:
            return "We'd like to display something but someone (most likely you) tampered" \
                    " with the GET request."
    if request.GET.get("dp"):
        dp = request.GET.get("dp")
    # TODO build release articles button (underConstruction -> false)
    f: Form = Form()
    f.action_url = "/admin/actions/alter-article-group"
    if grp:
        f.action_url += "?gid=" + str(grp.id)
    else:
        f.action_url += "?gid=-1"
    f.action_url += "&dp=" + dp
    f.add(PlainText("Name: "))
    if grp:
        f.add(TextField(name="grpname", button_text=str(grp.group_name)))
    else:
        f.add(TextField(name="grpname"))
    f.add(PlainText("Default Price: "))
    f.add(TextField(name="defaultgrpprice", button_text=dp, do_cr_after_input=False))
    f.add(PlainText(" € ct<br />"))
    f.add(CheckBox(name="visible", text="Make all articles visible now."))
    f.add(CheckBox(name="forceupdate", text="Force an update of the defaults"))
    f.add(SubmitButton())
    a += render_error_panel(request)
    a += f.render_html(request)
    if grp:
        # We're editing a group an hence need to display the matrix
        if Article.objects.all().filter(group=grp).filter(underConstruction=True).count() > 0:
            a += '<h6><img src="/staticfiles/frontpage/warning.png" class="icon" />' + \
                    'Not all Articles are released yet.</h6><br />'
        a += get_article_matrix_form(request, grp, defprice=dp)
    a += "</div>"
    return a


