
from raven import Client, breadcrumbs

client = Client('http://bf4fb0b826264238a6f8578dbd59c7f8:4048359898054eca8b8edb6a00fcf135@127.0.0.1:9000/2')

client.context.merge({'user': {
        'email': '1@11.com',
        'name': '1'

        },
    'extra': {'1': '11111'}
})

# client.captureMessage('123')
try:
    raise EOFError
except EOFError:
    pass
    client.captureException()


from raven.handlers.logging import SentryHandler

# Manually specify a client
# client = Client(...)
handler = SentryHandler(client)
import logging
logger = logging.getLogger(__name__)
logger.addHandler(handler)

logger.error('AAAAA', extra={
    'user': {'email': 'test@test.com'},
    'tags': {'database': '1.0'},
    'extra': {'111': '1111111'},
    '222': '23456'
})
# breadcrumbs.record('12345')
