import sys
import os
import pkgutil
import importlib
import argparse

# Imports centrais (mantém o core da DSL)
from frontend.lexer_pt    import lexer
from frontend.parser_pt   import parser
from semantic             import validar_services, SemanticError
from generator            import gerar_yml

# Tópicos de help em Português (incluindo 'variavel')
HELP_TOPICS = {
    'variavel': (
        'Uso: variavel NOME = "valor"\n'
        'Declara variável global para uso como ${NOME} no arquivo.'
    ),
    'serviço': (
        'Uso: serviço "nome" { ... }\n'
        'Define um serviço e abre o bloco de parâmetros.'
    ),
    'imagem': (
        'Uso: imagem "nome[:tag]"\n'
        'Define a imagem Docker do serviço.'
    ),
    'construir': (
        'Uso: construir "caminho"\n'
        'Define o diretório de build para gerar a imagem.'
    ),
    'argumentos': (
        'Uso: argumentos("CHAVE","VALOR",...)\n'
        'Define pares de variáveis para o build.'
    ),
    'nome_container': (
        'Uso: nome_container "nome"\n'
        'Define o nome do container gerado.'
    ),
    'reiniciar': (
        'Uso: reiniciar "always|on-failure|unless-stopped"\n'
        'Define a política de reinício do serviço.'
    ),
    'comando': (
        'Uso: comando ["cmd","arg1",...]\n'
        'Substitui o comando padrão do container.'
    ),
    'ponto_entrada': (
        'Uso: ponto_entrada ["script","arg1",...]\n'
        'Define o entrypoint do container.'
    ),
    'env': (
        'Uso: env("VAR","valor",...)\n'
        'Define variáveis de ambiente no container.'
    ),
    'arquivo_env': (
        'Uso: arquivo_env "arquivo.env"\n'
        'Importa um arquivo de variáveis (.env).'
    ),
    'portas': (
        'Uso: portas(80:80,443:443,...)\n'
        'Mapeia portas host:container.'
    ),
    'expor': (
        'Uso: expor(80,443,...)\n'
        'Define portas expostas pelo container.'
    ),
    'volume': (
        'Uso: volume "/caminho/no/container"\n'
        'Define mount de volume para persistência.'
    ),
    'dependentes': (
        'Uso: dependentes("serv1","serv2")\n'
        'Define ordem de inicialização.'
    ),
    'redes': (
        'Uso: redes("rede1","rede2")\n'
        'Associa o serviço a redes Docker.'
    ),
    'rotulos': (
        'Uso: rotulos("chave","valor",...)\n'
        'Define labels/metadados para o container.'
    ),
    'dir_trabalho': (
        'Uso: dir_trabalho "/workspace"\n'
        'Define o working_dir dentro do container.'
    ),
    'usuario': (
        'Uso: usuario "user"\n'
        'Define qual usuário fará a execução.'
    ),
    'hosts_extras': (
        'Uso: hosts_extras("host:ip",...)\n'
        'Adiciona entradas em /etc/hosts.'
    ),
    'limites': (
        'Uso: limites("nofile",1024,...)\n'
        'Define ulimits do container.'
    ),
}

ALL_COMMANDS = list(HELP_TOPICS.keys())

def print_help(topic=None):
    if not topic:
        sys.stdout.write("\nComandos disponíveis:\n")
        for cmd in ALL_COMMANDS:
            sys.stdout.write(f"  - {cmd}\n")
        sys.stdout.write("\nUse `help <comando>` para detalhes.\n\n")
        return

    key = topic
    if key not in HELP_TOPICS:
        if key + 's' in HELP_TOPICS:
            key = key + 's'
        elif key.endswith('s') and key[:-1] in HELP_TOPICS:
            key = key[:-1]

    if key in HELP_TOPICS:
        sys.stdout.write(f"\n{HELP_TOPICS[key]}\n\n")
    else:
        sugestoes = [c for c in ALL_COMMANDS if c.startswith(topic)]
        if sugestoes:
            sys.stdout.write(f"\nComando '{topic}' não encontrado. Talvez:\n")
            for s in sugestoes:
                sys.stdout.write(f"  - {s}\n")
            sys.stdout.write("\n")
        else:
            sys.stdout.write(f"\n❌ Ajuda não disponível para '{topic}'.\n\n")

def main():
    parser_top = argparse.ArgumentParser(prog='dangui', add_help=False)
    subs = parser_top.add_subparsers(dest='cmd')

    # Descobre plugins em commands/ ao lado deste script
    script_dir    = os.path.dirname(os.path.abspath(__file__))
    commands_path = os.path.join(script_dir, 'commands')
    for _, module_name, _ in pkgutil.iter_modules([commands_path]):
        mod = importlib.import_module(f'commands.{module_name}')
        if hasattr(mod, 'add_arguments'):
            mod.add_arguments(subs)

    args = parser_top.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
