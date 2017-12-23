from django.http import HttpRequest
from ..models import Settings
from ..uitools.body import render_user_link


def render_settings_page(request: HttpRequest):
    m: Settings = Settings.objects.get(SName='frontpage.ui.navbar.content')
    a = '''<div class="w3-row w3-padding-64 w3-twothird w3-container">
    <h3 class="w3-text-teal">Header content</h3>At the moment the header contains
    the following content:<p><code>%S%</code></p><br />It was last modified by: %U%
    <br /><a href="/admin/settings/edit-header"><img src="/staticfiles/frontpage/edit.png"
    alt="edit" class="button-img"/></a>
    </div>'''.replace('%S%', m.property).replace('%U%', render_user_link(m.changedByUser))
    m = Settings.objects.get(SName='frontpage.ui.footer.content')
    a += '''<div class="w3-row w3-padding-64 w3-twothird w3-container">
    <h3 class="w3-text-teal">Footer content</h3>At the moment the header contains
    the following content:<p><code>%S%</code></p><br />It was last modified by: %U%
    </div>'''.replace('%S%', m.property).replace('%U%', render_user_link(m.changedByUser))
    return a
