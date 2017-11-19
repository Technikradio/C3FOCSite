from ..models import GroupReservation, Article, ArticleRequested
from django.http import HttpRequest


def render_process_wizard(request: HttpRequest):
    a = '<div class="admin-popup">'
    page = 0
    if request.GET.get("page"):
        page = int(request.GET["page"])
    if not request.GET.get("reservation_id"):
        return '<div class="error-panel"><h3>Error: No reservation provided.</h3></div>'
    rid: int = int(request.GET["reservation_id"])
    r: GroupReservation = GroupReservation.objects.get(pk=rid)
    res_count: int = ArticleRequested.objects.filter(RID=r).count()
    a += "Created by: " + r.createdByUser.displayName + "< br/>"
    a += '<div class="notes">'
    a += r.notes
    a += '</div><br />'
    if page + 1 > res_count:
        a += '<a href="/admin/reservations/finish?reservation_id=' + str(r.pk) + '" class="button">Finish</a><br />'
    else:
        ar: ArticleRequested = ArticleRequested.objects.filter(RID=r)[page]
        at: Article = ar.AID
        a += 'Article: ' + str(at.description) + '<br />'
        a += 'Quantity: ' + str(ar.amount) + '<br />'
        a += 'Notes:<div class="notes">'
        a += ar.notes
        a += '</div><br /><br />'
        a += '<a href="/admin/reservations/process?reservation_id=' + str(rid) + '&page=' + str(page + 1) + '" ' \
             'class="button">Next</a>'
    a += '</div>'
    return a

