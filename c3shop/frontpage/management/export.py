from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from ..models import GroupReservation, Article, ArticleRequested
from .magic import timestamp
import logging
import qrcode

logger = logging.getLogger(__name__)

NOTES_STYLE = ParagraphStyle('notesstyle', fontSize=11)
ARTICLE_NOTES_STYLE = ParagraphStyle('notesstyle', fontSize=11)


def generateQRLink(link: str):
    qr = qrcode.QRCode(version=None, error_correction = qrcode.constants.ERROR_CORRECT_H, box_size = 30, border = 4)
    qr.add_data(link)
    qr.make(fit=True)
    return qr.make_image()


def renderSideStrip(p: canvas.Canvas, r: GroupReservation):
    p.setFont("Helvetica", 9)
    p.rotate(90)
    p.drawString(34, -25, "Reservation #" + str(r.id) + ' - Created at: ' + str(r.timestamp) + ' - Pickup date: ' + str(r.pickupDate))
    p.rotate(270)


def renderTableHeader(p: canvas.Canvas, y: int):
    p.line(50, y, A4[0] - 50, y)
    p.line(50, y - 25, A4[0] - 50, y - 25)
    p.drawString(55, y - 15, "Article")
    p.drawString(155, y - 15, "Quantity")
    p.drawString(235, y - 15, "Notes")
    p.drawString(A4[0] - 61, y - 15, "X")
    p.line(50, y, 50, y - 25)
    p.line(150, y, 150, y - 25)
    p.line(230, y, 230, y - 25)
    p.line(A4[0] - 65, y, A4[0] - 65, y - 25)
    p.line(A4[0] - 50, y, A4[0] - 50, y - 25)
    return y - 25


def renderArticleRequest(p: canvas.Canvas, arequested: ArticleRequested, y: int):
    a: Article = arequested.AID
    p.line(50, y, A4[0] - 50, y)
    p.drawString(55, y - 15, str(a.description))
    p.drawString(155, y - 15, str(arequested.amount))
    text = Paragraph(str(arequested.notes).replace("\n", "<br />"), style=ARTICLE_NOTES_STYLE)
    textwidth, textheight = text.wrapOn(p, A4[0] - 300, A4[1] - 100)
    text.drawOn(p, 235, y - 5 - textheight)
    r = y - 15 - textheight
    # render table lines
    p.line(50, r, A4[0] - 50, r)
    p.line(50, y, 50, r)
    p.line(150, y, 150, r)
    p.line(230, y, 230, r)
    p.line(A4[0] - 65, y, A4[0] - 65, r)
    p.line(A4[0] - 50, y, A4[0] - 50, r)
    # render check box (still easyer to do with lines that with PDF rects
    p.line(A4[0] - 62, y - 3, A4[0] - 53, y - 3)
    p.line(A4[0] - 62, y - 12, A4[0] - 53, y - 12)
    p.line(A4[0] - 62, y - 3, A4[0] - 62, y - 12)
    p.line(A4[0] - 53, y - 3, A4[0] - 53, y - 12)
    return r


def exportOrderToPDF(request: HttpRequest, res):
    # Setup the canvas
    reservations = []
    try:
        for r in res:
            logger.info("Exporting reservation: " + str(r))
            reservations.append(GroupReservation.objects.get(id=int(r)))
    except Exception as e:
        logger.exception(e)
        return HttpResponseForbidden("The requested reservation(s) do not seam to exist.<br />" + str(e))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="FOC-Orders_' + timestamp() + '.pdf"'
    buffer = BytesIO()
    p : canvas = canvas.Canvas(buffer, pagesize=A4, pageCompression=0)
    # Render PDF
    w, h = A4
    p.setTitle("C3FOC - Reservations")
    p.setAuthor("The robots in slavery by " + request.user.username)
    p.setSubject("This document, originally created at " + timestamp() + ", contains the requested reservations")
    for reservation in reservations:
        r: GroupReservation = reservation # Just for the sake of having a shourtcut
        if r.open and not r.ready:
            page = 1
            renderSideStrip(p, r)
            p.setFont("Helvetica", 14)
            # Render header
            p.drawString(25, h - 35, "Reservation by: " + str(r.createdByUser.displayName))
            p.line(25, h - 45, w - 25, h - 45)
            # render qr code
            i = generateQRLink(request.build_absolute_uri('/') + "admin/confirm?back_url=/admin/reservations&forward_url=/admin/reservations/finish&payload=" + str(r.id))
            p.drawInlineImage(i, w - 150, h - 175, 125, 125)
            p.setFont("Helvetica", 11)
            #text = p.beginText(30, h - 75)
            #text.textLines(r.notes)
            #p.drawText(text)
            text = Paragraph(r.notes.replace("\n", "<br />"), style=NOTES_STYLE)
            textwidth, textheight = text.wrapOn(p, w - 200, h - 250)
            text.drawOn(p, 30, h - 75 - textheight)
            cy = h - 100 - textheight
            if cy > h - 200:
                # Make sure to not draw over the qr code
                cy = h - 200
            cy = renderTableHeader(p, cy)
            for arequest in ArticleRequested.objects.filter(RID=r):
                if cy < 75:
                    cy = h - 55
                    if page == 1:
                        p.drawString(35, 35, "Page " + str(page))
                    else:
                        p.drawString(w - 75, h - 35, "Page " + str(page))
                    p.showPage()
                    page += 1
                    renderSideStrip(p, r)
                    p.setFont("Helvetica", 14)
                    p.drawString(25, h - 35, "Reservation by: " + str(r.createdByUser.displayName))
                    p.line(25, h - 45, w - 25, h - 45)
                    p.setFont("Helvetica", 11)
                cy = renderArticleRequest(p, arequest, cy)
            p.showPage() # End page here (one per request)
    #Close the canvas
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

