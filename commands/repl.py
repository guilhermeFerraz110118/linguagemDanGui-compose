import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from frontend.lexer_pt    import lexer
from frontend.parser_pt   import parser
from semantic             import validar_services, SemanticError

name = 'repl'
help = 'Inicia o shell interativo da DSL'

def add_arguments(subparsers):
    p = subparsers.add_parser(name, help=help, add_help=False)
    p.set_defaults(func=run)

def run(args):
    keywords = [
        'variavel','serviço','imagem','construir','argumentos','nome_container',
        'reiniciar','comando','ponto_entrada','env','arquivo_env',
        'portas','expor','volume','dependentes','redes','rotulos',
        'dir_trabalho','usuario','hosts_extras','limites','{','}','(',')',','
    ]
    completer = WordCompleter(keywords, ignore_case=True)
    session = PromptSession('dangui> ', completer=completer)
    print("🔎 REPL iniciado. Digite 'exit' ou 'quit' para sair.\n")
    buffer = []
    while True:
        try:
            line = session.prompt()
        except (EOFError, KeyboardInterrupt):
            break
        if line.strip().lower() in ('exit','quit'):
            break
        buffer.append(line)
        text = "\n".join(buffer)
        try:
            services = parser.parse(text, lexer=lexer)
            try:
                validar_services(services)
                print("✔ Sintaxe e semântica OK")
            except SemanticError as se:
                print(f"⚠️ Semântico: {se}")
            buffer = []
        except Exception:
            # aguarda mais linhas
            continue
    print("\n👋 Saindo do REPL")
    sys.exit(0)
