import math

class FormObject:
    object_name = ""

    def generate_html_code(self, form: Form):
        return self.object_name

    def __init__(self, name: str = ""):
        """
        This constructor initializes a new FormObject. It takes the name of the object as its only parameter
        :type name: str
        """
        super.__init__()
        self.object_name = name


class Form:
    action_url = ""
    method = "post"
    content = []

    def add_content(self, f_object: FormObject):
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


class PlainText(FormObject):
    text = ""

    def __init__(self, document_text: str = "", name: str = ""):
        super.__init__(name=name)
        self.text = document_text

    def generate_html_code(self, form: Form):
        return self.text


class FieldGroup(FormObject):
    text = ""
    content = []

    def __init__(self, name="", text=""):
        super.__init__(name=name)
        self.text = text

    def add_content(self, f_object: FormObject):
        self.content.append(f_object)

    def generate_html_code(self, form: Form):
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
    maxlenght = 0
    minimum = math.NaN
    maximum = math.NaN
    regex_pattern = None

    do_cr_after_input = True
    required = True

    def __init__(self, button_text="", name="", field_type="text", do_cr_after_input=True, required=True):
        super.__init__(name=name)
        self.button_text = button_text
        self.input_type = field_type
        self.do_cr_after_input = do_cr_after_input
        self.required = required

    def generate_html_code(self, form: Form):
        a = '<input type="' + self.input_type + '"'
        if not self.object_name == "":
            a += ' name="' + self.object_name + '"'
        if not self.button_text == "":
            a += ' value="' + self.button_text + '"'
        if self.maxlenght > 0:
            a += ' maxlenght="' + str(self.maxlenght) + '"'
        if self.minimum == math.NaN:
            a += ' min="' + str(self.minimum) + '"'
        if self.maximum == math.NaN:
            a += ' min="' + str(self.maximum) + '"'
        if self.regex_pattern:
            a += ' pattern="' + self.regex_pattern + '"'
        if self.required:
            a += ' required="' + str(self.required).lower() + '"'
        a += "/>"
        if self.do_cr_after_input:
            a += '<br />'
        return a


class TextField(InputField):

    def __init__(self, button_text="", name="", do_cr_after_input=True):
        super.__init__(button_text=button_text, name=name, do_cr_after_input=do_cr_after_input, field_type="text")


class PasswordField(InputField):

    def __init__(self, button_text="", name="", do_cr_after_input=True):
        super.__init__(button_text=button_text, name=name, do_cr_after_input=do_cr_after_input, field_type="password")


class EmailField(InputField):

    def __init__(self, button_text="", name="", do_cr_after_input=True):
        super.__init__(button_text=button_text, name=name, do_cr_after_input=do_cr_after_input, field_type="email")


class SubmitButton(InputField):

    def __init__(self, button_text="OK", name="", do_cr_after_input=True):
        super.__init__(button_text=button_text, name=name, do_cr_after_input=do_cr_after_input, field_type="submit")


class RadioList(FormObject):

    group = None
    do_cr_at_end = None

    def __init__(self, name="", elements=[], text="", do_cr_at_end=True):
        super.__init__(name=name)
        self.group = FieldGroup(name=name, text=text)
        item = 0
        total = len(elements)
        for rb in elements:
            item += 1
            is_last = False
            if total - item == 0:
                is_last = True
            self.group.add_content(InputField(button_text=rb, name=name, field_type="radio",
                                              do_cr_after_input=False))
            self.group.add_content(PlainText(' ' + rb))
            if not is_last:
                self.group.add_content(PlainText('<br />'))
        self.do_cr_at_end = do_cr_at_end

    def generate_html_code(self, form: Form):
        if self.do_cr_at_end:
            return self.group.generate_html_code() + "<br/>"
        else:
            return self.group.generate_html_code()


class TextArea(FormObject):
    colums = 0
    rows = 0
    label_content = None
    text = ""
    placeholder = ""

    def __init__(self, name="", max_colums=0, max_rows=0, label_text=None, text="", placeholder: str = ""):
        super.__init__(name=name)
        self.colums = max_colums
        self.rows = max_rows
        self.label_content = label_text
        self.text = text
        self.placeholder = placeholder

    def generate_html_code(self, form: Form):
        a = None
        if not self.label_content is None:
            a = '<label for="' + self.object_name + '">' + self.label_content + '</label><textarea id="' + \
                self.object_name + '" '
        else :
            a = '<textarea '
        a += 'name="' + self.object_name + '"'
        if self.colums > 0:
            a += ' cols="' + str(self.colums) + '"'
        if self.rows > 0:
            a += ' rows="' + str(self.rows) + '"'
        if self.placeholder != "":
            a += ' placeholder="' + str(self.placeholder) + '"'
        a += '>' + self.text + '</textarea>'
        return a


class NumberField(InputField):

    def __init__(self, button_text="", name="", do_cr_after_input=True):
        super.__init__(button_text=button_text, name=name, do_cr_after_input=do_cr_after_input, field_type="number")
