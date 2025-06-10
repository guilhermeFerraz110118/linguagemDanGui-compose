import ply.yacc as yacc
from frontend.lexer_pt import tokens, lexer

class Servico:
    def __init__(self, nome, params):
        self.nome = nome
        self.params = params

def p_project(p):
    "project : lista_servicos"
    p[0] = p[1]

def p_lista_servicos_servico(p):
    "lista_servicos : servico lista_servicos"
    p[0] = [p[1]] + p[2]

def p_lista_servicos_empty(p):
    "lista_servicos : empty"
    p[0] = []

def p_servico(p):
    "servico : SERVICO STRING LBRACE lista_params RBRACE"
    p[0] = Servico(p[2].strip('"'), p[4])

def p_lista_params_param(p):
    "lista_params : param lista_params"
    p[0] = [p[1]] + p[2]

def p_lista_params_empty(p):
    "lista_params : empty"
    p[0] = []

def p_param(p):
    """
    param : IMAGEM STRING
          | CONSTRUIR STRING
          | ARGUMENTOS LPAREN arg_list RPAREN
          | NOME_CONTAINER STRING
          | REINICIAR STRING
          | COMANDO '[' string_list ']'
          | PONTO_ENTRADA '[' string_list ']'
          | ENV LPAREN string_list RPAREN
          | ARQUIVO_ENV STRING
          | PORTAS LPAREN port_list RPAREN
          | EXPOR LPAREN num_list RPAREN
          | VOLUME STRING
          | DEPENDENTES LPAREN string_list RPAREN
          | REDES LPAREN string_list RPAREN
          | ROTULOS LPAREN string_list RPAREN
          | DIR_TRABALHO STRING
          | USUARIO STRING
          | HOSTS_EXTRAS LPAREN string_list RPAREN
          | LIMITES LPAREN ulimit_list RPAREN
    """
    chave = p[1]
    if chave == 'imagem':
        p[0] = ('image', p[2].strip('"'))
    elif chave == 'construir':
        p[0] = ('build', p[2].strip('"'))
    elif chave == 'argumentos':
        p[0] = ('args', p[3])
    elif chave == 'nome_container':
        p[0] = ('container_name', p[2].strip('"'))
    elif chave == 'reiniciar':
        p[0] = ('restart', p[2].strip('"'))
    elif chave == 'comando':
        p[0] = ('command', p[3])
    elif chave == 'ponto_entrada':
        p[0] = ('entrypoint', p[3])
    elif chave == 'env':
        p[0] = ('env', p[3])
    elif chave == 'arquivo_env':
        p[0] = ('env_file', p[2].strip('"'))
    elif chave == 'portas':
        p[0] = ('ports', p[3])
    elif chave == 'expor':
        p[0] = ('expose', p[3])
    elif chave == 'volume':
        p[0] = ('volume', p[2].strip('"'))
    elif chave == 'dependentes':
        p[0] = ('depends_on', p[3])
    elif chave == 'redes':
        p[0] = ('networks', p[3])
    elif chave == 'rotulos':
        p[0] = ('labels', p[3])
    elif chave == 'dir_trabalho':
        p[0] = ('working_dir', p[2].strip('"'))
    elif chave == 'usuario':
        p[0] = ('user', p[2].strip('"'))
    elif chave == 'hosts_extras':
        p[0] = ('extra_hosts', p[3])
    elif chave == 'limites':
        p[0] = ('ulimits', p[3])

def p_arg_list_single(p):
    "arg_list : STRING COMMA STRING"
    key, val = p[1].strip('"'), p[3].strip('"')
    p[0] = [(key, val)]

def p_arg_list_rec(p):
    "arg_list : STRING COMMA STRING COMMA arg_list"
    key, val = p[1].strip('"'), p[3].strip('"')
    p[0] = [(key, val)] + p[5]

def p_string_list_single(p):
    "string_list : STRING"
    p[0] = [p[1].strip('"')]

def p_string_list_rec(p):
    "string_list : STRING COMMA string_list"
    p[0] = [p[1].strip('"')] + p[3]

def p_port_list_single(p):
    "port_list : NUMBER ':' NUMBER"
    p[0] = [(int(p[1]), int(p[3]))]

def p_port_list_rec(p):
    "port_list : NUMBER ':' NUMBER COMMA port_list"
    head = (int(p[1]), int(p[3]))
    p[0] = [head] + p[5]

def p_num_list_single(p):
    "num_list : NUMBER"
    p[0] = [int(p[1])]

def p_num_list_rec(p):
    "num_list : NUMBER COMMA num_list"
    p[0] = [int(p[1])] + p[3]

def p_ulimit_list_single(p):
    "ulimit_list : STRING NUMBER"
    p[0] = [(p[1].strip('"'), int(p[2]))]

def p_ulimit_list_rec(p):
    "ulimit_list : STRING NUMBER COMMA ulimit_list"
    head = (p[1].strip('"'), int(p[2]))
    p[0] = [head] + p[4]

def p_empty(p):
    "empty :"
    p[0] = []

def p_error(p):
    if p:
        print(f"Erro sintático próximo a '{p.value}' na linha {p.lineno}")
    else:
        print("Erro sintático: fim de arquivo inesperado")

parser = yacc.yacc()
