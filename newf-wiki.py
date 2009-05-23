import newf

from urllib import quote, unquote
from wiki import Wiki

wiki = Wiki()

def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quote;')

def layout(title, body):
    return "<html><head><title>%s</title></head><body><h1>%s</h1>%s</body></html>" % (title, title, body)

def index(request):
    return newf.Response(layout("All Pages", "<ul>%s</ul>" % "".join(
        '<li><a href="/view/%s">%s</a></li>' % (quote(name), esc(name)) 
            for name in wiki.pages())))

def view(request, name):
    name = unquote(name)
    return newf.Response(layout(esc(name), 
        Wiki.format(wiki.get_page(name), lambda n: "/view/%s" % quote(n)) +
        '<p><a href="/edit/%s">Edit</a></p>' % quote(name)))

def edit(request, name):
    name = unquote(name)
    return newf.Response(layout("Edit " + esc(name), """
    <form method="post" action="/save">
    <input type="hidden" name="name" value="%s"/>
    <textarea name="text" cols="60" rows="15">%s</textarea><br/>
    <input type="submit" value="Save"/>
    or <a href="/view/%s">Cancel</a>
    </form>""" % (
        esc(name),
        esc(wiki.get_page(name)),
        quote(name))))

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