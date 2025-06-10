# linguagemDanGui-compose
Linguagem de domínio específico em Português para gerar, validar e automatizar arquivos docker-compose.yml com análise léxica, sintática e semântica.

# Compose-DSL

Compose-DSL é uma linguagem específica de domínio (DSL) em Português que simplifica a criação e manutenção de arquivos `docker-compose.yml`. Implementada em Python com PLY, a Compose-DSL oferece:

- **Sintaxe de alto nível:** blocos `serviço`, `imagem`, `portas`, `volume`, `env`, `redes`, entre outros  
- **Validação integrada:** análise léxica, sintática e semântica capturando erros antes do deploy  
- **Modo REPL interativo:** feedback em tempo real e sugestões contextuais  
- **Snippets e modelos:** comandos `modelo web`, `modelo db`, `modelo api` para acelerar o scaffold  
- **Gerador de YAML:** produção automática de `docker-compose.yml` (versão 3.8) pronto para execução  
- **CLI assistida:** `help`, `compilar`, `setup compose`, `repl`, `variavel`  

### Começando

```bash
git clone https://github.com/seu-usuario/compose-dsl.git
cd compose-dsl
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
python main.py novo          # Scaffold inicial
python main.py compilar meu_compose.dsl
docker-compose up -d
