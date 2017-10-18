from django.http import HttpRequest
from .form import Form, FileUpload, PlainText, TextField, TextArea


def render_single_form(request: HttpRequest):
    f: Form = Form()
    f.is_file_handler = True
    f.action_url = "/admin/actions/add-single-media"
    f.add_content(PlainText('<div>'))
    f.add_content(PlainText("Image headline: "))
    f.add_content(TextField(name="headline"))
    f.add_content(PlainText("Media category: "))
    f.add_content(TextField(name="category"))
    f.add_content(PlainText("Image text:<br />"))
    f.add_content(TextArea(name="text"))
    f.add_content(PlainText("Please select your file: "))
    f.add_content(FileUpload(name="file", multiple=False))
    f.add_content(PlainText('</div>'))
    return f.render_html()


def render_multiple_form(request: HttpRequest):
    f: Form = Form()
    f.is_file_handler = True
    f.action_url = "/admin/actions/add-bulk-media"
    f.add_content(PlainText("Shared image category: "))
    f.add_content(TextField(name="category"))
    f.add_content(PlainText("Select your files: "))
    f.add_content(FileUpload(name="files", multiple=True))
    return f.render_html()


def render_upload_page(request: HttpRequest):
    a = "You must decide to upload a single file or a bunch."
    if request.GET.get("hint"):
        a += "<div><p3>There was an error uploading the file(s):</p3>" + str(request.GET["hint"]) + "</div>"
    a += render_single_form(request)
    a += render_multiple_form(request)
    return a
