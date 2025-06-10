import sys
import re
from frontend.lexer_pt import lexer
from frontend.parser_pt import parser
from semantic import validar_services, SemanticError
from generator import gerar_yml

name = 'compilar'
help = 'Compila um arquivo .dsl em docker-compose.yml'

def preprocess(text):
    """
    Extrai declarações de variáveis:
      variavel NOME = "valor"
    Remove essas linhas e faz replace de ${NOME} no restante.
    """
    vars = {}
    lines = []
    for line in text.splitlines():
        m = re.match(r'\s*variavel\s+([A-Za-z_]\w*)\s*=\s*"([^"]*)"', line)
        if m:
            vars[m.group(1)] = m.group(2)
        else:
            lines.append(line)
    processed = "\n".join(lines)
    def repl(m):
        key = m.group(1)
        return vars.get(key, m.group(0))
    return re.sub(r'\$\{(\w+)\}', repl, processed)

def add_arguments(subparsers):
    p = subparsers.add_parser(name, help=help, add_help=False)
    p.add_argument('arquivo', help='Arquivo .dsl de entrada')
    p.add_argument('-h','--help', action='store_true', dest='want_help',
                   help='Mostra este help específico')
    p.set_defaults(func=run)

def run(args):
    if args.want_help:
        sys.stdout.write(f"\nUso: compilar arquivo.dsl\n\n")
        sys.exit(0)

    if not args.arquivo.endswith('.dsl'):
        print("❌ Extensão inválida. Use arquivo.dsl")
        sys.exit(1)

    try:
        raw = open(args.arquivo, encoding='utf-8').read()
    except FileNotFoundError:
        print(f"❌ Arquivo '{args.arquivo}' não encontrado.")
        sys.exit(1)

    texto = preprocess(raw)
    services = parser.parse(texto, lexer=lexer)

    try:
        validar_services(services)
    except SemanticError as e:
        print("❌ Erro semântico:", e)
        sys.exit(1)

    gerar_yml(services, output='docker-compose.yml')
    print("✔ Docker Compose gerado: docker-compose.yml")
