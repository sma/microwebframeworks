import newf

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
    ${block c}<form method="post" action="/save">
    <input type="hidden" name="name" value="${name|e}"/>
    <textarea name="text" cols="60" rows="15">${text|e}</textarea><br/>
    <input type="submit" value="Save"/>
    or <a href="/view/${name|u}">Cancel</a>
    </form>${endblock}"""

def template(tmpl, **kwargs):
    return newf.Response(T.render(T.get(tmpl), kwargs))

def index(request):
    return template("index", pages=wiki.pages())

def view(request, name):
    name = unquote(name)
    return template("view", name=name, text=Wiki.format(wiki.get_page(name),
        lambda n: "/view/%s" % quote(n)))

def edit(request, name):
    name = unquote(name)
    return template("edit", name=name, text=wiki.get_page(name))

def save(request):
    if request.method != 'POST':
        return newf.Response(status_code=405)
    name = request.POST.getfirst('name')
    wiki.set_page(name, request.POST.getfirst('text'))
    return newf.ResponseRedirect("/view/%s" % quote(name))

application = newf.Application((
    (r'/index$', index),
    (r'/view/(?P<name>.*)$', view),
    (r'/edit/(?P<name>.*)$', edit),
    (r'/save$', save),
))

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('', 8000, application)
    server.serve_forever()