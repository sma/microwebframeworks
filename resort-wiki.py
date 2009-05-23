class Index(resort.Component):
    def __init__(self, wiki):
        self.wiki = wiki
    
    def render(self, html):
        html.heading("All Pages")
        with html.unorderd_list():
            for page in self.wiki.pages():
                html.list_item(html.anchor(call=html.bind(self.view, page), text=page))

    def view(self, name):
        self.goto(View(self.wiki.get_page(name)))

class View(resort.Component):
    def __init__(self, page):
        self.page = page
    
    def render(self, html):
        html.heading(self.page.title)
        with html.div():
            html.raw(self.page.text_html(lambda s: html.url_for(html.bind(self.view, s))))
        with html.paragraph():
            html.anchor(call=self.edit, text="Edit")
    
    def view(self, name):
        self.goto(View(self.page.wiki.get_page(name)))
    
    def edit(self):
        self.open(Edit(self.page))

class Edit(resort.Component):
    def __init__(self, page):
        self.page = page
    
    def render(self, html):
        html.heading("Edit ", self.page.title)
        with html.form():
            html.textarea(key='text', object=self.page, cols=60, rows=15)
            with html.paragraph():
                html.button(call=self.save, text="Save")
                html.text(" or ")
                html.anchor(call=self.close, text="Cancel")
    
    def save(self):
        self.page.save()
        self.close()

if __name__ == '__main__':
    resort.route("index", lambda: Index(Wiki()))
    resort.run()