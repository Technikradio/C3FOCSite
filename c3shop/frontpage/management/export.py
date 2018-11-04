from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse, HttpRequest

def exportOrderToPDF(request: HttpRequest):
    # Setup the canvas
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    buffer = BytesIO()
    p : canvas = canvas.Canvas(buffer)
    # Render PDF
    #Close the canvas
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

