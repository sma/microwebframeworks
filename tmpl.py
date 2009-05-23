import re

from urllib import quote, unquote

def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quote;')

class Tmpl(object):
    @classmethod
    def get(self, path): return getattr(self, "_" + path.replace(".html", ""))

    @classmethod
    def render(self, tmpl, c):
        def block(m):
            name = "block %s" % m.group(1)
            c[name] = c.get(name).replace("${super}", m.group(2)) if c.get(name) else m.group(2)
            return c[name]
        tmpl = re.sub(r"(?s)\$\{block +(\w+?)\}(.*?)\$\{endblock\}", block, tmpl)

        m = re.search(r"\$\{extends +(\S+?)\}", tmpl)
        if m: return self.render(self.get(m.group(1)), dict(c))

        def loop(m):
            def cwith(key, value): c1 = dict(c); c1[key] = value; return c1
            return "".join(self.render(m.group(3), cwith(m.group(1), item)) for item in c.get(m.group(2), ()))
        tmpl = re.sub(r"(?s)\$\{for +(\w+) +in +(\w+)\}(.*?)\$\{endfor\}", loop, tmpl)

        def repl(m):
            return {'e': esc, 'u': quote}.get(m.group(2), str)(str(c.get(m.group(1)) or ""))
        return re.sub(r"\$\{(\w+?)(?:\|([ue]))?\}", repl, tmpl)