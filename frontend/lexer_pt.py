import ply.lex as lex

tokens = (
    'SERVICO','IMAGEM','CONSTRUIR','ARGUMENTOS','NOME_CONTAINER',
    'REINICIAR','COMANDO','PONTO_ENTRADA','ENV','ARQUIVO_ENV',
    'PORTAS','EXPOR','VOLUME','DEPENDENTES','REDES','ROTULOS',
    'DIR_TRABALHO','USUARIO','HOSTS_EXTRAS','LIMITES',
    'STRING','NUMBER','LPAREN','RPAREN','LBRACE','RBRACE','COMMA',
)

literals = [':','[',']']

t_SERVICO        = r"serviço"
t_IMAGEM         = r"imagem"
t_CONSTRUIR      = r"construir"
t_ARGUMENTOS     = r"argumentos"
t_NOME_CONTAINER = r"nome_container"
t_REINICIAR      = r"reiniciar"
t_COMANDO        = r"comando"
t_PONTO_ENTRADA  = r"ponto_entrada"
t_ENV            = r"env"
t_ARQUIVO_ENV    = r"arquivo_env"
t_PORTAS         = r"portas"
t_EXPOR          = r"expor"
t_VOLUME         = r"volume"
t_DEPENDENTES    = r"dependentes"
t_REDES          = r"redes"
t_ROTULOS        = r"rotulos"
t_DIR_TRABALHO   = r"dir_trabalho"
t_USUARIO        = r"usuario"
t_HOSTS_EXTRAS   = r"hosts_extras"
t_LIMITES        = r"limites"

t_STRING = r'\"[^\"\n]*\"'
t_NUMBER = r"\d+"

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_COMMA  = r","

t_ignore         = " \t\r"
t_ignore_COMMENT = r"\#.*"

def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Erro léxico: caractere inesperado {t.value[0]!r} na linha {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
