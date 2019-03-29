from io import BytesIO

from django.http import HttpRequest, HttpResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas

from frontpage.management.magic import timestamp
from frontpage.models import Article


def export_reject_statistics(request: HttpRequest):
    # Begin PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="FOC-RejectStatistics_' + timestamp() + '.pdf"'
    buffer = BytesIO()
    w, h = landscape(A4)  # Reversed return values in order to produce landscape orientation
    p: canvas = canvas.Canvas(buffer, pagesize=landscape(A4), pageCompression=0)
    p.setTitle("C3FOC - Missing Merch statistics")
    p.setAuthor("The robots in slavery by " + request.user.username)
    p.setSubject("This document, originally created at " + timestamp(filestr=False) +
                 ", is a template for the missing merchandise statistics.")
    page = 1
    p.setFont("Helvetica", 11)
    # Render the Article list
    cy = h - 50
    for a in Article.objects.all():
        p.line(50, cy, w - 50, cy)
        p.drawString(55, cy - 10, "[" + str(a.id) + "]: " + str(a.description))
        p.line(50, cy - 50, w - 50, cy - 50)
        p.line(50, cy, 50, cy - 50)
        p.line(w - 50, cy, w - 50, cy - 50)
        cy -= 50
        if cy <= 65:
            # Break page
            p.drawString(50, 50, "Page " + str(page) + ", " + timestamp())
            p.showPage()
            page += 1
            cy = h - 50
    if page == 1:
        p.drawString(50, 50, timestamp(filestr=False))
    # Finish PDF
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response