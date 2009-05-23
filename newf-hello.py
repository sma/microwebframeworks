import newf
    
def hello(request, name="Welt"):
    return newf.Response("Hallo %s" % name)
    
application = newf.Application((
        (r'^/hello$', hello),
        (r'^/hello/(?P<name>.*)$', hello),
))

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('', 8000, application)
    server.serve_forever()