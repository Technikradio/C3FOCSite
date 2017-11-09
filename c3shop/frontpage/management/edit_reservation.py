from django.http import HttpRequest, HttpResponseRedirect
import json

RESERVATION_CONSTRUCTION_COOKIE_KEY: str = "c3shop.frontpage.reservation.cookiekey"


def add_article_action(request: HttpRequest, default_foreward_url: str):
    forward_url = default_foreward_url
    # TODO fix
    current_reservation = json.loads(request.COOKIES.get(RESERVATION_CONSTRUCTION_COOKIE_KEY))
    id: int = int(request.POST.get("article_id"))
    quantity : int = int(request.POST["quantity"])
    current_reservation.get("articles").append({"id": id, "quantity": quantity})
    response = HttpResponseRedirect(forward_url)
    response.set_cookie(RESERVATION_CONSTRUCTION_COOKIE_KEY, json.dumps(current_reservation, indent=4))
    return response


def create_reservation_action(request: HttpRequest):
    """
    This function is used to add a reservation to the database from the
    cookie stored inside the client. This function automatically crafts
    the required HttpResponse.
    """
    # TODO fix
    pass


def manipulate_reservation_action(request: HttpRequest):
    """
    This function is used to alter the reservation beeing build inside
    a cookie. This function automatically crafts the required response.
    """
    pass
