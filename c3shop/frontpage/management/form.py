
class FormObject:
    object_name = ""

    def generate_html_code(self, form):
        return self.object_name

    def __init__(self, name=""):
        self.object_name = name


class Form:
    action_url = ""
    method = "post"
    content = []

    def add_content(self, f_object):
        self.content.append(f_object)

    def render_html(self):
        a = '<form method="%method%"'.replace("%method%", self.method)
        if not self.action_url == "":
            a += ' action="%action%">'.replace("%action%", self.action_url)
        else:
            a += '>'
        for c in self.content:
            a += c.generate_html_code(self)
        a += "</form>"
        return a


class Text(FormObject):
    text = ""

    def __init__(self, document_text="", name=""):
        super(name=name)
        self.text = document_text

    def generate_html_code(self, form):
        return self.text


class FieldGroup(FormObject):
    text = ""
    content = []

    def __init__(self, name="", text=""):
        super(name=name)
        self.text = text

    def add_content(self, f_object):
        self.content.append(f_object)

    def generate_html_code(self, form):
        a = "<fieldset>"
        if not self.text == "":
            a += '<legend>' + self.text + '</legend>'
        for c in self.content:
            a += c.generate_html_code(self)
        a += "</fieldset>"
        return a


class InputField(FormObject):
    button_text = ""
    input_type = ""  # The type of the text field ( later used by PasswordTextField, EmailTextField,
                     # NumberTextField, etc.)
    do_cr_after_input = True

    def __init__(self, button_text="", name="", field_type="text", do_cr_after_input=True):
        super(name=name)
        self.button_text = button_text
        self.input_type = field_type
        self.do_cr_after_input = do_cr_after_input

    def generate_html_code(self, form):
        a = '<input type="' + self.input_type + '"'
        if not self.object_name == "":
            a += ' name="' + self.object_name + '"'
        if not self.button_text == "":
            a += ' value="' + self.button_text + '"'
        a += "/>"
        if self.do_cr_after_input:
            a += '<br />'
        return a


class TextField(InputField):

    def __init__(self, button_text="", name="", do_cr_after_input=True):
        super(button_text=button_text, name=name, do_cr_after_input=do_cr_after_input, field_type="text")


class SubmitButton(InputField):

    def __init__(self, button_text="OK", name="", do_cr_after_input=True):
        super(button_text=button_text, name=name, do_cr_after_input=do_cr_after_input, field_type="submit")

# TODO implement radio button list
