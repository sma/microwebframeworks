import mnml

from wiki import Wiki
from tmpl import Tmpl, quote, unquote

wiki = Wiki()

class T(Tmpl):
    _base = """<html>
    <head><title>Wiki</title></head>
    <body><h1>${block t}${endblock}</h1>${block c}${endblock}</body>
    </html>"""
    
    _index = """${extends base}
    ${block t}All Pages${endblock}
    ${block c}<ul>
    ${for page in pages}<li><a href="/view/${page|u}">${page|e}</a></li>${endfor}
    </ul>${endblock}"""
    
    _view = """${extends base}
    ${block t}${name|e}${endblock}
    ${block c}${text}<p><a href="/edit/${name|u}">Edit</a></p>${endblock}"""
    
    _edit = """${extends base}
    ${block t}Edit ${name|e}${endblock}
    ${block c}<form method="post" action="/edit/${name|u}">
    <textarea name="text" cols="60" rows="15">${text|e}</textarea><br/>
    <input type="submit" value="Save"/>
    or <a href="/view/${name|u}">Cancel</a>
    </form>${endblock}"""

def template(tmpl, **kwargs):
    return mnml.HttpResponse(T.render(T.get(tmpl), kwargs))

class Index(mnml.RequestHandler):
    def GET(self):
        return template("index", pages=wiki.pages())

class View(mnml.RequestHandler):
    def GET(self, name):
        name = unquote(name)
        return template("view", name=name,
            text=Wiki.format(wiki.get_page(name), lambda n: "/view/%s" % quote(n)))

class Edit(mnml.RequestHandler):
    def GET(self, name):
        name = unquote(name)
        return template("edit", name=name, text=wiki.get_page(name))
    
    def POST(self, name):
        name = unquote(name)
        wiki.set_page(name, self.request.POST.getfirst('text'))
        return mnml.HttpResponseRedirect("/view/%s" % quote(name))

application = mnml.TokenBasedApplication((
    ('/index', Index),
    ('/view/:name', View),
    ('/edit/:name', Edit),
))

if __name__ == '__main__':
    mnml.development_server(application)