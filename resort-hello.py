class Hello(resort.Component):
    def __init__(self, name):
        self.name = name

    def render(self, html):
        html.text("Hello, ", self.name)

if __name__ == '__main__':
    resort.route("/hello", lambda: Hello())
    resort.route("/hello/:name", lambda name: Hello(name))
    resort.run()