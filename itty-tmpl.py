from itty import *
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
    return T.render(T.get(tmpl), kwargs)

@get("/index")
def index(request):
    return template("index", pages=wiki.pages())

@get("/view/(?P<name>.+)")
def view(request, name):
    name = unquote(name)
    return template("view", name=name,
        text=Wiki.format(wiki.get_page(name), lambda n: "/view/%s" % quote(n)))

@get("/edit/(?P<name>.+)")
def edit(request, name):
    name = unquote(name)
    return template("edit", name=name, text=wiki.get_page(name))

@post("/edit/(?P<name>.+)")
def save(request, name):
    name = unquote(name)
    wiki.set_page(name, request.POST['text'])
    raise Redirect("/view/%s" % quote(name))

if __name__ == '__main__':
    run_itty()