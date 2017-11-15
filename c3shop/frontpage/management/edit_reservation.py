from django.http import HttpRequest
from .form import Form, PlainText
from .reservation_actions import EMPTY_COOKY_VALUE
from .reservation_actions import RESERVATION_CONSTRUCTION_COOKIE_KEY
from ..models import Article
import json

def render_edit_page(request: HttpRequest):
    """
    This method will return the reservation edit page.
    The first form will be used in order to manipulate global reservation
    settings. The table below will list all selected articles including
    the amount and notes.
    """
    current_reservation = None
    if RESERVATION_CONSTRUCTION_COOKIE_KEY in request.COOKIES:
        current_reservation = json.loads(request.COOKIES[RESERVATION_CONSTRUCTION_COOKIE_KEY])
    else:
        current_reservation = json.loads(EMPTY_COOKY_VALUE)
    f: Form = Form()
    f.action_url = "/admin/actions/alter-current-reservation"
    f.add_content(PlainText("<h3>Edit reservation: </h3>"))
    # TODO implement global settings form here
    a = f.render_html()
    a += '<br />Add article: <a href="/admin/reservations/select-article">Add an ' + \
            'Article to the reservation</a>'
    a += "<table><tr><th> Headline </th><th> Amount </th><th> Notes </th></tr>"
    for art in current_reservation["articles"]:
        art: Article = Article.objects.get(int(art["id"]))
        a += "<tr><td>" + art.description + "</td><td>" + str(art["quantity"]) + "</td>"
        a += "<td>" + str(art["notes"]) + "</td></tr>"
    a += "</table>"
    return a
