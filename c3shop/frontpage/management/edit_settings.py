from django.http import HttpRequest
from ..models import Settings
from .form import PlainText, TextArea, SubmitButton, Form, TextField


def render_text_based_panel(request: HttpRequest, setting: str):
    s: Settings = Settings.objects.get(SName=setting)
    f: Form = Form()
    f.action_url = "/admin/actions/set-header"
    f.add_content(PlainText('<h3 class="w3-text-teal">Edit header content:</h3>'))
    f.add_content(TextArea(name="property", label_text="Edit the content of the nav bar:",
        text=s.property, placeholder="Please define the content of the header using JSON"))
    f.add_content(PlainText("Please specify the reason you change this setting: "))
    f.add_content(TextField(name="reason"))
    f.add_content(SubmitButton())
    a = '<div class="w3-row w3-padding-64 w3-twothird w3-container">'
    a += f.render_html(request)
    a += '</div>'
    return a


def render_header_edit_panel(request: HttpRequest):
    return render_text_based_panel(request, 'frontpage.ui.navbar.content')


def render_footer_edit_panel(request: HttpRequest):
    return render_text_based_panel(request, 'frontpage.ui.footer.content')
