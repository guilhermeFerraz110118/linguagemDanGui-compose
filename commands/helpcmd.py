import sys
from main import print_help

name = 'help'
help = 'Exibe ajuda geral ou de um comando específico'

def add_arguments(subparsers):
    p = subparsers.add_parser(name, help=help, add_help=False)
    p.add_argument('topic', nargs='?', default=None,
                   help='Comando para detalhar')
    p.set_defaults(func=run)

def run(args):
    print_help(args.topic)
    sys.exit(0)
