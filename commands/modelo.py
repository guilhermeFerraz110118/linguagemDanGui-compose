import sys

name = 'modelo'
help = 'Exibe modelos rápidos de serviços para agilizar seu DSL'

MODEL_SNIPPETS = {
    'web': (
        'serviço "web" {\n'
        '  imagem "nginx:latest"\n'
        '  portas(80:80)\n'
        '  reiniciar "always"\n'
        '}\n'
    ),
    'db': (
        'serviço "db" {\n'
        '  imagem "mysql:5.7"\n'
        '  env("MYSQL_ROOT_PASSWORD","root")\n'
        '  volume "/var/lib/mysql"\n'
        '  reiniciar "unless-stopped"\n'
        '}\n'
    ),
    'api': (
        'serviço "api" {\n'
        '  construir "./api"\n'
        '  env("FLASK_ENV","production")\n'
        '  portas(5000:5000)\n'
        '  dependentes("db")\n'
        '}\n'
    ),
}

def add_arguments(subparsers):
    p = subparsers.add_parser(name, help=help, add_help=False)
    p.add_argument('tipo', nargs='?', choices=MODEL_SNIPPETS.keys(),
                   help='Tipo de modelo: ' + ', '.join(MODEL_SNIPPETS.keys()))
    p.set_defaults(func=run)

def run(args):
    if not args.tipo:
        sys.stdout.write("Modelos disponíveis:\n")
        for k in MODEL_SNIPPETS:
            sys.stdout.write(f"  • {k}\n")
        sys.exit(0)
    snippet = MODEL_SNIPPETS[args.tipo]
    sys.stdout.write(f"\n# Modelo '{args.tipo}':\n{snippet}\n")
    sys.exit(0)
