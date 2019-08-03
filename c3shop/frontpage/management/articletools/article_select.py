import traceback
import logging

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from frontpage.models import Article, ArticleGroup, GroupReservation, Profile
from frontpage.management.page_skeleton import render_headbar, render_footer
from frontpage.management.form import Form, NumberField, TextArea, SubmitButton, PlainText
from frontpage.management.magic import get_article_pcs_free
from frontpage.uitools.body import get_type_string, render_price
from ..magic import get_current_user
from ..grouptools.edit_group import get_article_dict


logger = logging.getLogger(__file__)


def get_group_variations(grp: ArticleGroup):
    sizes = []
    types = []
    for article in Article.objects.all().filter(group=grp):
        if article.size not in sizes:
            sizes.append(article.size)
        if article.type not in types:
            types.append(article.type)
    sizesstr = ""
    typesstr = ""
    sizes.sort()
    types.sort()
    for s in sizes:
        sizesstr += " " + s
    for t in types:
        typesstr += " " + get_type_string(t)
    return sizesstr + " ", typesstr + " "

def render_article_selection_page(request: HttpRequest):
    rid: str = str(request.GET.get("rid"))
    known_groups = []
    page = 1
    if request.GET.get('page'):
        page = int(request.GET['page'])
    items_per_page = 50
    if request.GET.get('objects'):
        items_per_page = int(request.GET["objects"])
    total_items = Article.objects.all().filter(visible=True).filter(underConstruction=False).count()
    max_page = total_items / items_per_page
    if max_page < 1:
        max_page = 1
    if page > max_page:
        page = max_page
    start_range = 1 + page * items_per_page
    if start_range > total_items:
        start_range = 0
    end_range = (page + 1) * items_per_page
    a = render_headbar(request, title="Select article")
    a += '<div class="w3-row w3-padding-64 w3-twothird w3-container">'
    a += '<h3>Please select your desired article</h3><table><tr><th>Select</th><th>Preview</th>' \
            + '<th>Title</th><th>Size</th><th>Type</th></tr>'
    objects = Article.objects.filter(visible=True).filter(underConstruction=False).filter(pk__range=(start_range, end_range))
    for article in objects:
        group = article.group
        if group is None:
            s: str = None
            p = article.flashImage
            if p:
                s = p.lowResFile
            else:
                s = "/staticfiles/frontpage/no-image.png"
            a += '<tr><td><a href="/admin/reservations/article-detail-select?article_id=' + str(article.pk)
            a += '&rid=' + rid + '"><img src="/staticfiles/frontpage/order-article.png" class="button-img"/>' + \
                    '</a></td><td><img src="'
            a += s + '" /></td><td>' + article.description + '</td><td>' + article.size + '</td><td>' + \
                get_type_string(article.type) + '</td></tr>'
        elif group not in known_groups:
            known_groups.append(group)
            s: str = None
            p = group.group_flash_image
            if p:
                s = p.lowResFile
            else:
                s = "/staticfiles/frontpage/no-image.png"
            sizes, types = get_group_variations(group)
            a += '<tr><td><a href="/admin/reservations/article-detail-select?article_id=' + str(article.pk)
            a += '&rid=' + rid + '"><img src="/staticfiles/frontpage/order-article.png" ' + \
                    'class="button-img"/></a></td><td><img src="'
            a += s + '" /></td><td>' + group.group_name + '</td><td>' + sizes + '</td><td>' + \
                    types + '</td></tr>'
    a += '</table>'
    if page > 1:
        a += '<a href="' + request.path + '?page=' + str(page - 1) + '&objects=' + str(objects) + \
             '" class="button">Previous page </a>'
    if page < max_page:
        a += '<a href="' + request.path + '?page=' + str(page + 1) + '&objects=' + str(objects) + \
             '" class="button">Next page </a>'
    a += '</div>' + render_footer(request)
    return HttpResponse(a)


def render_detail_selection(request: HttpRequest):
    try:
        res: GroupReservation = -1
        user: Profile = None
        try:
            res = GroupReservation.objects.get(id=int(request.GET["rid"]))
            user = get_current_user(request)
            if res.createdByUser != user and user.rights < 2:
                raise Exception("Editing foreign reservation")
        except Exception as e:
            logger.warning("\nUser " + str(user) + " from IP " + str(request.META['REMOTE_ADDR']) + \
                    " Caused an exception: " + traceback.format_exc() + "\n\n")
            return redirect("/admin/?msgid=editreservation.invalidrequest;" + str(e))
        a: Article = Article.objects.get(pk=int(request.GET["article_id"]))
        f: Form = Form()
        if a.group is None:
            f.action_url = "/admin/actions/add-article-to-reservation?article_id=" + str(a.pk) + \
                        "&redirect=/admin/reservations/edit"
            f.add(PlainText("Price: " + render_price(a.price) + "<br />"))
            f.add_content(PlainText("Specify amount: "))
            f.add_content(NumberField(name="quantity", minimum=1, maximum=get_article_pcs_free(a),
                button_text="1"))
            f.add_content(PlainText("Maybe add some optional notes:"))
            f.add_content(TextArea(name="notes", label_text="Notes:", text=""))
            f.add_content(PlainText("<br />"))
        else:
            grp = a.group
            f.action_url = "/admin/actions/add-article-to-reservation?group_id=" + str(grp.pk) + \
                    "&redirect=/admin/reservations/edit"
            sizes, types, sizesdict = get_article_dict(grp)
            f.add(PlainText("<table><thead><tr><th> Version </th>"))
            for s in sizes:
                f.add(PlainText("<th>" + str(s) + "</th>"))
            f.add(PlainText("</tr></thead><tbody>"))
            for t in types:
                f.add(PlainText("<tr><td>" + get_type_string(t) + "</td>"))
                for s in sizes:
                    f.add(PlainText("<td>"))
                    if sizesdict[s].get(t):
                        quantity, price, aid, description, visible = sizesdict[s][t]
                        if not visible:
                            f.add(PlainText("Currently not avaiable"))
                        pcsfree = get_article_pcs_free(Article.objects.get(pk=aid))
                        if visible and pcsfree > 0:
                            f.add(PlainText("Price: " + render_price(price) + "<br />"))
                            f.add_content(PlainText("Specify amount: "))
                            f.add_content(NumberField(name="quantity_" + str(aid), minimum=0, 
                                maximum=pcsfree, button_text="0"))
                            f.add_content(PlainText("Maybe add some optional notes:"))
                            f.add_content(TextArea(name="notes_" + str(aid), label_text="Notes:", text=""))
                        else:
                            f.add(PlainText("Unfortunately this article is already sold out."))
                    else:
                        f.add(PlainText("Currently not avaiable"))
                    f.add(PlainText("</td>"))
                f.add(PlainText("</tr>"))
            f.add(PlainText("</tbody></table><br />"))
        f.add_content(SubmitButton())
        a = render_headbar(request, title="Specify article details")
        a += '<div class=""><div class="w3-row w3-padding-64 w3-twothird w3-container">' \
            '<h3>Please specify further details:</h3>'
        a += f.render_html(request)
        a += '</div></div>' + render_footer(request)
        return HttpResponse(a)
    except Exception as e:
        return redirect("/admin/?error=" + str(e))
