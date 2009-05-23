from itty import *
from urllib import quote, unquote
from wiki import Wiki

wiki = Wiki()

def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quote;')

def layout(title, body):
    return "<html><head><title>%s</title></head><body><h1>%s</h1>%s</body></html>" % (
        title, title, body)

@get("/index")
def index(request):
    return layout("All Pages", "<ul>%s</ul>" % "".join(
        '<li><a href="/view/%s">%s</a></li>' % (quote(name), esc(name)) 
            for name in wiki.pages()))

@get("/view/(?P<name>.+)")
def view(request, name):
    name = unquote(name)
    return layout(name, 
        Wiki.format(wiki.get_page(name), lambda n: "/view/%s" % quote(n)) +
        '<p><a href="/edit/%s">Edit</a></p>' % quote(name))

@get("/edit/(?P<name>.+)")
def edit(request, name):
    name = unquote(name)
    return layout("Edit " + esc(name), """
    <form method="post" action="/edit/%s">
    <textarea name="text" cols="60" rows="15">%s</textarea><br/>
    <input type="submit" value="Save"/>
    or <a href="/view/%s">Cancel</a>
    </form>""" % (
        quote(name),
        esc(wiki.get_page(name)),
        quote(name)))

@post("/edit/(?P<name>.+)")
def save(request, name):
    name = unquote(name)
    wiki.set_page(name, request.POST['text'])
    raise Redirect("/view/%s" % quote(name))

if __name__ == '__main__':
    run_itty()