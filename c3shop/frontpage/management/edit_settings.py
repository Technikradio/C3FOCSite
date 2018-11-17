from django.http import HttpRequest
from ..models import Settings
from .form import PlainText, TextArea, SubmitButton, Form, TextField


def render_text_based_panel(request: HttpRequest, setting: str, a1: str, a2: str, action: str):
    s: Settings = Settings.objects.get(SName=setting)
    f: Form = Form()
    f.action_url = action
    f.add_content(PlainText('<h3 class="w3-text-teal">' + a1 + '</h3>'))
    f.add_content(TextArea(name="property", label_text=a2,
        text=s.property, placeholder="Please define the content of the header using JSON"))
    f.add_content(PlainText("Please specify the reason you change this setting: "))
    f.add_content(TextField(name="reason"))
    f.add_content(SubmitButton())
    return f.render_html(request)
    


def render_header_edit_panel(request: HttpRequest):
    return '<div class="admin-popup w3-row w3-padding-64 w3-twothird w3-container">' + render_text_based_panel(request, 
            'frontpage.ui.navbar.content', 'Edit header content:',
            'Edit the content of the nav bar:', "/admin/actions/set-header")


def render_footer_edit_panel(request: HttpRequest):
    return render_text_based_panel(request, 'frontpage.ui.footer.content', 'Edit footer content:',
            'Edit the content of the footer:', "/admin/actions/set-footer", begin=False) + '</div>'

