from juno import *
from wiki import Wiki
from tmpl import Tmpl, quote, unquote

init({'use_templates': False, 'use_db': False})

config('get_template_handler', lambda path: T.get(path))
config('render_template_handler', lambda tmpl, **kwargs: T.render(tmpl, kwargs))

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
    
    _404 = """${extends base}${block t}404 not found${endblock}${block c}${error}${endblock}"""
    
    _500 = """${extends base}${block t}500 server error${endblock}${block c}${error}${endblock}"""

@get("/index")
def index(request):
    template("index", pages=wiki.pages())

@get("/view/:name")
def view(request, name):
    name = unquote(name)
    template("view", name=name, text=Wiki.format(wiki.get_page(name), lambda n: "/view/%s" % quote(n)))

@get("/edit/:name")
def edit(request, name):
    name = unquote(name)
    template("edit", name=name, text=wiki.get_page(name))

@post("/edit/:name")
def save(request, name):
    name = unquote(name)
    wiki.set_page(name, request.input()['text'])
    redirect("/view/%s" % quote(name))

if __name__ == '__main__':
    run()