
"""
The entry point to run sentry with source code.
The real entry points are in src/sentry/run_source/

Usage:

> python run.py -m server
> python run.py -m worker

"""

import os
import sys

import click

sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
from sentry.run_source import run_server, run_simple_server, run_works, run_install_static


@click.command()
@click.option('--module', '-m', default='server')
def main(module='server'):
    m = globals().get('run_' + module)
    if len(sys.argv) > 1 and sys.argv[1] in ('--module', '-m'):
        sys.argv.pop(1)
        sys.argv.pop(1)
    if m:
        m.main()
    else:
        click.echo('No module %s' % module)


if __name__ == '__main__':
    main()