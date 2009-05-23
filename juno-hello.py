from juno import *

init({'use_templates': False, 'use_db': False})

@route(['/hello', '/hello/:name'])
def hello(web, name="qo'"):
    return "%s nuqneH" % name

run()
