# commands/setup.py

import sys

name = 'setup'
help = 'Guia passo-a-passo para instalar Docker Compose'

def add_arguments(subparsers):
    p = subparsers.add_parser(name, help=help, add_help=False)
    p.add_argument('topic', nargs='?', choices=['compose'], default='compose',
                   help='Assunto do guia (atualmente só "compose")')
    p.set_defaults(func=run)

def run(args):
    if args.topic == 'compose':
        print("\n📦 Guia de Instalação do Docker Compose\n")
        print("1) Windows:")
        print("   - Baixe o instalador em:")
        print("     https://docs.docker.com/compose/install/")
        print("   - Execute o instalador e siga as instruções da UI.\n")
        print("2) Linux:")
        print("   - Executar no terminal:")
        print("     sudo curl -L "
              "https://github.com/docker/compose/releases/download/1.29.2/"
              "docker-compose-$(uname -s)-$(uname -m) "
              "-o /usr/local/bin/docker-compose")
        print("   - Depois:")
        print("     sudo chmod +x /usr/local/bin/docker-compose\n")
        print("3) macOS:")
        print("   - Se usar Homebrew:")
        print("       brew install docker-compose")
        print("   - Ou baixe o binário em:")
        print("       https://docs.docker.com/compose/install/\n")
        print("✅ Verifique com: docker-compose --version\n")
        sys.exit(0)
    else:
        print(f"❌ Guia não disponível para '{args.topic}'.")
        sys.exit(1)
