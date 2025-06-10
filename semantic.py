class SemanticError(Exception):
    """Erro semântico da DSL Dangui."""
    pass

def suggest_name(base, existing):
    """
    Gera uma sugestão de nome baseado em `base`, acrescentando _1, _2, ...
    até encontrar um que não esteja em `existing`.
    """
    i = 1
    while True:
        cand = f"{base}_{i}"
        if cand not in existing:
            return cand
        i += 1

def validar_services(services):
    """
    Valida a lista de serviços:
      - nomes de serviços únicos (com sugestão em caso de duplicata)
      - imagem ou build obrigatório
      - portas dentro do intervalo 1–65535
      - dependências existem
      - volumes começam com '/'
      - coleta de volumes e redes (para geração)
    """
    # Tabela de símbolos: nome -> Serviço
    symbol_table = {}
    for svc in services:
        if svc.nome in symbol_table:
            alt = suggest_name(svc.nome, symbol_table)
            raise SemanticError(
                f"Serviço duplicado: '{svc.nome}'. Sugestão: use '{alt}'."
            )
        symbol_table[svc.nome] = svc

    volumes = set()
    networks = set()

    # Valida cada serviço
    for svc in services:
        # imagem ou build obrigatório
        has_img = any(p[0] == 'image' for p in svc.params)
        has_bld = any(p[0] == 'build' for p in svc.params)
        if not (has_img or has_bld):
            raise SemanticError(f"'{svc.nome}' precisa de imagem ou construir.")

        for key, val in svc.params:
            if key == 'depends_on':
                # cada dependência deve estar na tabela
                for dep in val:
                    if dep not in symbol_table:
                        raise SemanticError(
                            f"'{svc.nome}' depende de desconhecido '{dep}'."
                        )

            elif key == 'ports':
                # checa range de cada porta
                for h, c in val:
                    if not (1 <= h <= 65535 and 1 <= c <= 65535):
                        raise SemanticError(
                            f"Porta inválida em '{svc.nome}': {h}:{c}."
                        )

            elif key == 'volume':
                # volume path deve iniciar com '/'
                if not val.startswith('/'):
                    raise SemanticError(
                        f"Volume inválido em '{svc.nome}': '{val}'. "
                        "Caminho deve começar com '/'."
                    )
                # coleta nome de volume único
                vol_name = f"{svc.nome}_vol0"
                if vol_name in volumes:
                    # sugestão de nome de volume alternativo
                    alt = suggest_name(vol_name, volumes)
                    raise SemanticError(
                        f"Nome de volume duplicado: '{vol_name}'. Sugestão: '{alt}'."
                    )
                volumes.add(vol_name)

            elif key == 'networks':
                # coleta todas as redes referenciadas
                for net in val:
                    networks.add(net)

    # Retorna os símbolos (pode ser útil futuramente)
    return {
        'services': symbol_table,
        'volumes': volumes,
        'networks': networks
    }
