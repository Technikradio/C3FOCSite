
class FormObject:
    name = ""

    def generate_html_code(self, form):
        pass


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
