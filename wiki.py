import re, os

class Wiki(object):
    def __init__(self, base="pages"):
        if not os.path.exists(base):
            os.makedirs(base)
        self.base = base
    
    def pages(self):
        return list(sorted([n.decode("quopri") for n in os.listdir(self.base)]))
    
    def get_page(self, name):
        try:
            return open(os.path.join(self.base, name.encode("quopri"))).read()
        except IOError:
            return ""
    
    def set_page(self, name, text):
        with open(os.path.join(self.base, name.encode("quopri")), "w") as f: f.write(text)
    
    @staticmethod
    def format(text, quote=lambda name:name):
        def fmt(line):
            line = line.replace('&', '&amp;').replace('<', '&lt;')
            line = re.sub(r"^# (.*)$", "<h1>\\1</h1>", line)
            line = re.sub(r"^\* (.*)$", "<ul><li>\\1</li></ul>", line)
            line = re.sub(r"^    (.*)$", "<pre>\\1</pre>", line)
            line = re.sub(r"^([^<].*)$", "<p>\\1</p>", line)
            line = re.sub(r"\*(.*?)\*", "<strong>\\1</strong>", line)
            line = re.sub(r"\[(.*?)(?:\|(.*?))?\]", lambda m:'<a href="%s">%s</a>' % (
                quote(m.group(1)), m.group(2) or m.group(1)), line)
            return line
        text = "\n".join(fmt(line) for line in text.splitlines())
        text = re.sub(r"</(\w+)>\n<\1>", "\n", text)
        return text

