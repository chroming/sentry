
from wsgiref import simple_server
from sentry.wsgi import application


def main():
    server = simple_server.make_server('', 9000, application)
    server.serve_forever()


if __name__ == '__main__':
    main()