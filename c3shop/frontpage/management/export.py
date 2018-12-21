from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, StreamingHttpResponse
from django.core.exceptions import ObjectDoesNotExist
from ..models import GroupReservation, Article, ArticleRequested, Media, Post
from .magic import timestamp
from .media_actions import PATH_TO_UPLOAD_FOLDER_ON_DISK
import logging
import qrcode
import base64
import traceback

logger = logging.getLogger(__name__)

NOTES_STYLE = ParagraphStyle('notesstyle', fontSize=11)
ARTICLE_NOTES_STYLE = ParagraphStyle('articlestyle', fontSize=11)
INFO_STYLE = ParagraphStyle(
        'infostyle', fontSize=9,
        border_color="#000000",
        border_width=1,
        border_padding=(7, 2, 20),
        border_radius=None,
        )


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


def renderArticleRequest(p: canvas.Canvas, arequested: ArticleRequested, y: int, retry=False):
    a: Article = arequested.AID
    text = Paragraph(str(arequested.notes).replace("\n", "<br />"), style=ARTICLE_NOTES_STYLE)
    textwidth, textheight = text.wrapOn(p, A4[0] - 300, A4[1] - 100)
    if textheight > (y - 50) and not retry:
        return y, arequested
    p.line(50, y, A4[0] - 50, y)
    p.drawString(55, y - 15, str(a.description))
    p.drawString(155, y - 15, str(arequested.amount))
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
    return r, None


def getPriceString(p):
    """
    :param: p This takes the price in cents an renderes it to a string
    :return: The price string as EUR
    """
    return '{:20,.2f}'.format(int(p) / 100) + ' €'


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
    if len(reservations) == 1:
        response['Content-Disposition'] = 'attachment; filename="FOC-Order_N°' + str(res[0]) + '.pdf"'
    else:
        response['Content-Disposition'] = 'attachment; filename="FOC-Orders_' + timestamp() + '.pdf"'
    buffer = BytesIO()
    p : canvas = canvas.Canvas(buffer, pagesize=A4, pageCompression=0)
    # Render PDF
    w, h = A4
    p.setTitle("C3FOC - Reservations")
    p.setAuthor("The robots in slavery by " + request.user.username)
    p.setSubject("This document, originally created at " + timestamp(filestr=False) + ", contains the requested reservations")
    for reservation in reservations:
        r: GroupReservation = reservation # Just for the sake of having a shourtcut
        if r.open and not r.ready:
            page = 1
            p.addOutlineEntry("[" + str(r.id) + "]" + str(r.createdByUser.displayName), "r" + str(r.id))
            p.bookmarkPage("r" + str(r.id))
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
            # render the responsible person info field
            contactinfo = "<b>Contact:</b> " + str(r.responsiblePerson) + " <b>Mail:</b> " + str(r.createdByUser.authuser.email)
            if r.createdByUser.dect != 0:
                contactinfo += " <b>DECT:</b> " + str(r.createdByUser.dect)
            if textheight > 150:
                # Render info box under the QR code
                text = Paragraph(contactinfo.replace("<b>", "<br /><b>"), style=INFO_STYLE)
                text.wrapOn(p, 125, 65)
                text.drawOn(p, w - 142, h - 200)
            else:
                # Render info box unter the notes
                text = Paragraph(contactinfo, style=INFO_STYLE)
                text.wrapOn(p, w - 200, 20)
                text.drawOn(p, 30, h - textheight - 100)
                textheight += 25
                pass
            #begin rendering of reservations
            cy = h - 100 - textheight
            if cy > h - 200:
                # Make sure to not draw over the qr code
                cy = h - 200
            cy = renderTableHeader(p, cy)
            summedRequest = {}
            for arequest in ArticleRequested.objects.filter(RID=r):
                if arequest.AID in summedRequest.keys():
                    summedRequest[arequest.AID] = arequest.amount + summedRequest[arequest.AID]
                    # print(str(arequest.AID) + " in dict. updating.")
                else:
                    summedRequest[arequest.AID] = arequest.amount
                    # print(str(arequest.AID) + " not in dictionary")
                cy, retryObject = renderArticleRequest(p, arequest, cy)
                if cy < 75 or (retryObject != None):
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
                    if retryObject != None:
                        cy, retryObject = renderArticleRequest(p, arequest, cy, retry=True)
            if cy < len(summedRequest) * 15 + 140:
                # We need a new page in order to render the invoice
                p.showPage()
                renderSideStrip(p, r)
                p.drawString(w - 75, h - 35, "Page " + str(page))
                page += 1
                p.setFont("Helvetica", 14)
                p.drawString(25, h - 35, "Reservation by: " + str(r.createdByUser.displayName))
                p.line(25, h - 45, w - 25, h - 45)
                p.setFont("Helvetica", 11)
                cy = h - 55
            else:
                cy -= 30
            # Finally render the invoice box
            # Render the table header
            p.line(45, cy, 45, cy - 15)
            p.line(w - 45, cy, w - 45, cy - 15)
            p.line(45, cy, w - 45, cy)
            p.line(45, cy - 15, w - 45, cy - 15)
            p.drawString(50, cy - 10, "Amount")
            p.drawString(100, cy - 10, "Article")
            p.drawString(250, cy - 10, "Single Item price")
            p.drawString(w - 175, cy - 10, "Sum")
            cy -= 15
            total: int = 0
            for a in summedRequest.keys():
                amount: int = summedRequest[a]
                total += int(a.price) * amount
                p.line(45, cy, 45, cy - 15)
                p.line(w - 45, cy, w - 45, cy - 15)
                p.drawString(100, cy - 10, a.description)
                p.drawString(50, cy - 10, str(amount))
                p.drawString(250, cy - 10, getPriceString(int(a.price)))
                p.drawString(w - 175, cy - 10, getPriceString(int(a.price) * amount))
                cy -= 15
            p.line(45, cy, w - 45, cy)
            p.line(45, cy, 45, cy - 15)
            p.line(w - 45, cy, w - 45, cy - 15)
            p.line(45, cy - 15, w - 45, cy - 15)
            p.drawString(50, cy - 10, "TOTAL:")
            p.drawString(100, cy - 10, "[EUR]")
            p.drawString(w - 175, cy - 10, getPriceString(total))
            # Signature of person who packed and person who checked
            cy -= 75
            p.line(55, cy, 235, cy)
            p.drawString(60, cy - 10, "Signature of person who packed")
            p.line(255, cy, 435, cy)
            p.drawString(260, cy - 10, "Signature of person who checked")
            p.showPage() # End page here (one per request)
    #Close the canvas
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def exportRejectstatistics(request: HttpRequest):
    # Begin PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="FOC-RejectStatistics_' + timestamp() + '.pdf"'
    buffer = BytesIO()
    w, h = landscape(A4) # Reversed return values in order to produce landscape orientation
    p : canvas = canvas.Canvas(buffer, pagesize=landscape(A4), pageCompression=0)
    p.setTitle("C3FOC - Missing Merch statistics")
    p.setAuthor("The robots in slavery by " + request.user.username)
    p.setSubject("This document, originally created at " + timestamp(filestr=False) + ", is a template for the mssing merchandise" \
            " statistics.")
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


"""
========================================================================================================
Begin Section of data export feature ===================================================================
========================================================================================================
There should be the consideration to put this into a separate file and use the print submodule for PDFs.
"""


class DataDumpIterator:

    step: int = 8
    payload = None

    def __iter__(self):
        self.step = 8
        self.payload = None
        return self

    def __next__(self):
        if self.step == 0:
            raise StopIteration
        elif self.step == 8:
            # Return stored images
            if self.payload == None:
                self.payload = 1 # Look up first id
            try:
                img = Media.objects.get(id=int(self.payload))
                a = '{"type" : "media", "data" : [ "category" : "'
                a += str(base64.b64encode(bytes(str(img.category), 'utf-8'))) + '", "headline" : "'
                a += str(base64.b64encode(bytes(str(img.headline), 'utf-8'))) + '", "text" : "'
                a += str(base64.b64encode(bytes(str(img.text), 'utf-8'))) + '", "timestamp" : "'
                # We'll not save the cached text here as it can be recreated
                a += str(base64.b64encode(bytes(str(img.uploadTimestamp), 'utf-8'))) + '", "highfilepath" : "'
                a += str(base64.b64encode(bytes(str(img.highResFile), 'utf-8'))) + '", "lowfilepath" : "'
                a += str(base64.b64encode(bytes(str(img.lowResFile), 'utf-8'))) + '", "highresfile" : "'
                f = open(PATH_TO_UPLOAD_FOLDER_ON_DISK + str(img.highResFile)[1:], "rb") # remove trailing /
                a += str(base64.b64encode(f.read())) + '", "lowresfile" : "'
                f.close()
                f = open(PATH_TO_UPLOAD_FOLDER_ON_DISK + str(img.lowResFile)[1:], "rb")
                a += str(base64.b64encode(f.read())) + '"]}\n'
                f.close()
                self.payload = int(self.payload) + 1
                return a
            except ObjectDoesNotExist:
                self.step -= 1
                self.payload = None
                return "#\n# We're finished with the media assets. Moving on...\n#\n"
            except Exception as e:
                self.step -= 1
                self.payload = None
                return "# Hit an exception. Assuming that we reached the end of the media assets.\n" \
                        "# Exception content: " + str(e).replace("\n", "") + "\n"  + traceback.format_exc().replace("\n", "\n# ")
            return "Hier könnten ihre bilder stehen.\n"
            pass
        elif self.step == 7:
            # Return articles
            if self.payload == None:
                self.payload = 1 # Look up first id
            try:
                art = Article.objects.get(id=int(self.payload))
                a = '{"type" : "article", "data" : [ "price" : "'
                a += str(base64.b64encode(bytes(str(art.price), 'utf-8'))) + '", "largeText" : "'
                a += str(base64.b64encode(bytes(str(art.largeText), 'utf-8'))) + '", "type" : "'
                a += str(base64.b64encode(bytes(str(art.type), 'utf-8'))) + '", "description" : "'
                a += str(base64.b64encode(bytes(str(art.description), 'utf-8'))) + '", "visible" : "'
                a += str(base64.b64encode(bytes(str(art.visible), 'utf-8'))) + '", "quantity" : "'
                a += str(base64.b64encode(bytes(str(art.quantity), 'utf-8'))) + '", "size" : "'
                a += str(base64.b64encode(bytes(str(art.size), 'utf-8'))) + '", "addedby" : "'
                try:
                    a += str(base64.b64encode(bytes(str(art.addedByUser.authuser.username), 'utf-8'))) + '", "flashimgid" : "'
                except Exception as e:
                    print(e)
                    a += str(base64.b64encode(bytes(str("admin"), 'utf-8'))) + '", "flashimgid" : "'
                try:
                    a += str(base64.b64encode(bytes(str(art.flashImage.id), 'utf-8'))) + '", "chestsize" : "'
                except:
                    a += str(base64.b64encode(bytes(str("none"), 'utf-8'))) + '", "chestsize" : "'
                a += str(base64.b64encode(bytes(str(art.chestsize), 'utf-8'))) + '"]}\n'
                self.payload = int(self.payload) + 1
                return a
            except ObjectDoesNotExist:
                self.step -= 1
                self.payload = None
                return "#\n# We're done with the articles. Moving on...\n#\n"
            except Exception as e:
                self.step -= 1
                self.payload = None
                return "# There was an exception while processing the articles. Jumping to the next job.\n" \
                        "# Exception content: " + str(e).replace("\n", "") + "\n" + traceback.format_exc().replace("\n", "\n# ")
            return "Hier könnten ihre Artikel stehen.\n"
        elif self.step == 6:
            # Saving posts to data dump
            if self.payload == None:
                self.payload = 1
            try:
                p = Post.objects.get(id=1)
                a = '{"type" : "post", "data" : [ "title" : "'
                a += str(base64.b64encode(bytes(str(p.title), 'utf-8'))) + '", "addedby" : "'
                try:
                    a += str(base64.b64encode(bytes(str(p.createdByUser.authuser.username), 'utf-8'))) + '", "username" : "'
                except:
                    a += str(base64.b64encode(bytes(str("admin"), 'utf-8'))) + '", "visible" : "'
                a += str(base64.b64encode(bytes(str(p.visibleLevel), 'utf-8'))) + '", "timestamp" : "'
                a += str(base64.b64encode(bytes(str(p.timestamp), 'utf-8'))) + '", "text" : "'
                a += str(base64.b64encode(bytes(str(p.text), 'utf-8'))) + '"]}\n'
                return a
            except ObjectDoesNotExist as e:
                self.step -= 1
                self.payload = None
                return "#\n# We're done with the posts. Moving on...\n#\n"
            except Exception as e:
                self.step -= 1
                self.payload = None
                return "# There was an exception while processing the posts. Jumping to the next job.\n" \
                        "# Exception content: " + str(e).replace("\n", "") + "\n" + traceback.format_exc().replace("\n", "\n# ")
            return "# Hier könnten ihre Posts stehen"
        else:
            # something went wrong
            if self.step < 0:
                self.step = 0
                return StopIteration
            self.step -= 1
            return self.__next__()


def get_dump_iterator():
    return iter(DataDumpIterator())


def request_data_dump(request: HttpRequest):
    response: StreamingHttpResponse = StreamingHttpResponse(get_dump_iterator())
    response['Content-Type'] = 'application/focdump-demformat'
    response['Content-Disposition'] = 'attachment; filename="c3foc-datadump-' + timestamp() + '.pxtz"'
    return response
