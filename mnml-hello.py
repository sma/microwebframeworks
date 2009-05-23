import mnml

class Hello(mnml.RequestHandler):
    def GET(self, name="World"):
        return mnml.HttpResponse("Hello, %s" % name)

application = mnml.TokenBasedApplication((
    ('/hello', Hello),
    ('/hello/:name', Hello),
))

if __name__ == '__main__':
    mnml.development_server(application)