import os
import sys
from datetime import datetime

name = 'novo'
help = 'Cria um novo projeto com estrutura básica da DSL'

TEMPLATE_FILES = {
    'main.py': "# … copie aqui seu main.py completo …\n",
    'meu_compose.dsl': (
        "# Seu primeiro projeto Dangui\n"
        'serviço "exemplo" {\n'
        '  imagem "alpine:latest"\n'
        '  comando ["echo","Olá Mundo"]\n'
        '}\n'
    ),
    'docs/GRAMATICA_PT.ebnf': "(* … gramática EBNF em PT … *)\n",
}

DIRS = ['frontend', 'commands', 'docs']

def add_arguments(subparsers):
    p = subparsers.add_parser(name, help=help, add_help=False)
    p.set_defaults(func=run)

def run(args):
    cwd = os.getcwd()
    for d in DIRS:
        os.makedirs(os.path.join(cwd, d), exist_ok=True)
    for rel, content in TEMPLATE_FILES.items():
        path = os.path.join(cwd, rel)
        if os.path.exists(path):
            print(f"❌ Já existe: {rel}")
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✔ Criado: {rel}")
    print(f"\nProjeto inicializado em {cwd} em {datetime.now():%Y-%m-%d %H:%M}")
    sys.exit(0)
