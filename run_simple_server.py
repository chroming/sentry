import logging
import celery

# from sentry.runner.commands.run import web
# from sentry.runner import main
from wsgiref import simple_server
from sentry.wsgi import application

# web.main()

# main()

server = simple_server.make_server('', 9000, application)
server.serve_forever()