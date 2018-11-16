from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from ..models import GroupReservation
import logging

logger = logging.getLogger(__name__)

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
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    buffer = BytesIO()
    p : canvas = canvas.Canvas(buffer, pagesize=A4, pageCompression=0)
    # Render PDF
    w, h = A4
    for reservation in reservations:
        r: GroupReservation = reservation # Just for the sake of having a shourtcut
        p.setFont("Helvetica", 14)
        p.rotate(180)
        p.drawString(10, 10, "Reservation by: " + str(r.createdByUser.displayName))
        p.line(0, 15, w, 15)
        # TODO generate finished link QR code
        text = p.beginText(15, 30)
        text.textLines(r.notes)
        p.drawText(text)
        p.showPage() # End page here (one per request)
    #Close the canvas
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

