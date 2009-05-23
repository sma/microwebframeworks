import djng

def hello(request, name="Welt"):
    return djng.Response("Hallo, %s!" % name)

app = djng.Router(
    (r'^hello$', hello),
    (r'^hello/(+*)$', hello),
)

if __name__ == '__main__':
    djng.serve(app, '0.0.0.0', 8000)