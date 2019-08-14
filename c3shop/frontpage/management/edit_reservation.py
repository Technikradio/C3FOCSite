from django.http import HttpRequest
from .form import Form, PlainText, Date, TextArea, SubmitButton
from .reservation_actions import EMPTY_COOKY_VALUE
from .reservation_actions import RESERVATION_CONSTRUCTION_COOKIE_KEY
from .magic import get_current_user
from ..models import Article, Profile, GroupReservation, ArticleRequested
import json


def render_edit_page(request: HttpRequest):
    """
    This method will return the reservation edit page.
    The first form will be used in order to manipulate global reservation
    settings. The table below will list all selected articles including
    the amount and notes. It will now require an database object
    """
    a = '<div class="admin-popup w3-twothird w3-padding-64 w3-row w3-container">'
    current_reservation = None
    u: Profile = get_current_user(request)
    if "rid" in request.GET:
        current_reservation = GroupReservation.objects.get(id=int(request.GET["rid"]))
        if current_reservation.createdByUser != u and u.rights < 2:
            return "You dont't habe the permission to review this reservation.</div>"
    f: Form = Form()
    f.action_url = "/admin/actions/alter-current-reservation?redirect=/admin/reservations/edit"
    f.add_content(PlainText("<h3>Edit reservation: </h3>"))
    f.add_content(PlainText("Enter date: "))
    f.add_content(PlainText("Notes:<br/>"))
    if current_reservation:
        f.add_content(TextArea(name="notes", placeholder="Write additional notes here.", text=current_reservation.notes))
    else:
        f.add_content(TextArea(name="notes", placeholder="Write additional notes here.", text=""))
    f.add_content(PlainText("<br/>"))
    f.add_content(SubmitButton())
    a += f.render_html(request)
    artnum = 0
    if current_reservation:
        a += '<br />Add article: <a href="/admin/reservations/select-article?rid=' + str (current_reservation.id) + \
                '"><img src="/staticfiles/frontpage/order-' \
             'article.png" class="button-img"/></a>'
        a += "<table><tr><th> Headline </th><th> Amount </th><th> Notes </th><th> Delete </th></tr>"
        i = 0
        for ar in ArticleRequested.objects.all().filter(RID=current_reservation):
            r_art: Article = ar.AID
            a += "<tr><td>" + r_art.description + "</td><td>" + str(ar.amount) + "</td>"
            a += "<td>" + str(ar.notes) + '</td><td><a href="/admin/actions/delete-article?id=' + str(ar.id) + \
                 '&rid=' + str(current_reservation.id) + '"><img src="/staticfiles/frontpage/delete.png" class="button-img"/></a></td></tr>'
            i += 1
        a += "</table>"
        artnum = i
        if current_reservation.notes and artnum > 0:
            a += '<br /><a href="/admin/confirm?back_url=' + str(request.get_full_path()) + '&payload=' + str(current_reservation.id) + \
                    '&forward_url=/admin/actions/save-current-reservation" class="button">Submit Reservation (final)</a>'
    a += '</div>'
    return a
