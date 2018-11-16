from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from ..models import GroupReservation
from .magic import timestamp
import logging
import qrcode

logger = logging.getLogger(__name__)


def generateQRLink(link: str):
    qr = qrcode.QRCode(version=None, error_correction = qrcode.constants.ERROR_CORRECT_H, box_size = 30, border = 4)
    qr.add_data(link)
    qr.make(fit=True)
    return qr.make_image()


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
            p.setFont("Helvetica", 9)
            p.rotate(90)
            p.drawString(34, -25, "Reservation #" + str(r.id))
            p.rotate(270)
            p.setFont("Helvetica", 14)
            # Render header
            p.drawString(25, h - 35, "Reservation by: " + str(r.createdByUser.displayName))
            p.line(25, h - 45, w - 25, h - 45)
            # render qr code
            i = generateQRLink(request.build_absolute_uri('/') + "admin/confirm?back_url=/admin/reservations&forward_url=/admin/reservations/finish&payload=" + str(r.id))
            p.drawInlineImage(i, w - 150, h - 175, 125, 125)
            # TODO generate finished link QR code
            text = p.beginText(30, h - 75)
            text.textLines(r.notes)
            p.drawText(text)
            p.showPage() # End page here (one per request)
    #Close the canvas
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

