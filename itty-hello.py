from itty import get, run_itty

@get("/hello")
@get("/hello/(?P<name>.*)")
def hello(request, name="mundus"):
    return "Salve, %s!" % name
    
run_itty()

