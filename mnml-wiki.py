import mnml

from urllib import quote, unquote
from wiki import Wiki

wiki = Wiki()

def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quote;')

def layout(title, body):
    return "<html><head><title>%s</title></head><body><h1>%s</h1>%s</body></html>" % (title, title, body)

class Index(mnml.RequestHandler):
    def GET(self):
        return mnml.HttpResponse(layout("All Pages", "<ul>%s</ul>" % "".join(
            '<li><a href="/view/%s">%s</a></li>' % (quote(name), esc(name)) 
                for name in wiki.pages())))

class View(mnml.RequestHandler):
    def GET(self, name):
        name = unquote(name)
        return mnml.HttpResponse(layout(esc(name), 
            Wiki.format(wiki.get_page(name), lambda n: "/view/%s" % quote(n)) +
            '<p><a href="/edit/%s">Edit</a></p>' % quote(name)))

class Edit(mnml.RequestHandler):
    def GET(self, name):
        name = unquote(name)
        return mnml.HttpResponse(layout("Edit " + esc(name), """
        <form method="post" action="/edit/%s">
        <textarea name="text" cols="60" rows="15">%s</textarea><br/>
        <input type="submit" value="Save"/>
        or <a href="/view/%s">Cancel</a>
        </form>""" % (
            quote(name),
            esc(wiki.get_page(name)),
            quote(name))))
    
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