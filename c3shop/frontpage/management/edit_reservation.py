from django.http import HttpRequest
from .form import Form, PlainText, Date, TextArea, SubmitButton
from .reservation_actions import EMPTY_COOKY_VALUE
from .reservation_actions import RESERVATION_CONSTRUCTION_COOKIE_KEY
from ..models import Article
import json


def render_edit_page(request: HttpRequest):
    """
    This method will return the reservation edit page.
    The first form will be used in order to manipulate global reservation
    settings. The table below will list all selected articles including
    the amount and notes. If no cookie is present but the GET-Value [id] it will load it.
    """
    current_reservation = None
    if RESERVATION_CONSTRUCTION_COOKIE_KEY in request.COOKIES:
        current_reservation = json.loads(request.COOKIES[RESERVATION_CONSTRUCTION_COOKIE_KEY])
    else:
        current_reservation = json.loads(EMPTY_COOKY_VALUE)
    f: Form = Form()
    f.action_url = "/admin/actions/alter-current-reservation?redirect=/admin/reservations/edit"
    f.add_content(PlainText("<h3>Edit reservation: </h3>"))
    # TODO implement global settings form here
    f.add_content(PlainText("Enter date: "))
    f.add_content(Date(name="pickup_date", date=current_reservation["pickup_date"]))
    f.add_content(PlainText("Notes:<br/>"))
    f.add_content(TextArea(name="notes", placeholder="Write additional notes here.", text=current_reservation["notes"]))
    f.add_content(PlainText("<br/>"))
    f.add_content(SubmitButton())
    a = f.render_html()
    a += '<br />Add article: <a href="/admin/reservations/select-article"><img src="/staticfiles/frontpage/order-' \
         'article.png" class="button-img"/></a>'
    a += "<table><tr><th> Headline </th><th> Amount </th><th> Notes </th></tr>"
    for art in current_reservation["articles"]:
        r_art: Article = Article.objects.get(pk=int(art["id"]))
        a += "<tr><td>" + r_art.description + "</td><td>" + str(art["quantity"]) + "</td>"
        a += "<td>" + str(art["notes"]) + "</td></tr>"
    a += "</table>"
    if current_reservation.get("notes") and current_reservation.get("pickup_date"):
        a += '<br /><a href="/admin/actions/save-current-reservation" class="button">Submit Reservation</a>'
    return a
