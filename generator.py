import yaml

def gerar_yml(services, output='docker-compose.yml'):
    """
    Gera o docker-compose.yml com cabeçalho de boas práticas e comentários explicativos.
    """
    doc = {
        'version': '3.8',
        'services': {},
    }
    vols, nets = set(), set()

    # Monta o bloco de serviços
    for svc in services:
        svc_dict = {}
        for key, val in svc.params:
            if key in ('image', 'build', 'restart', 'working_dir', 'user'):
                svc_dict[key] = val
            elif key == 'ports':
                svc_dict['ports'] = [f"{h}:{c}" for h, c in val]
            elif key == 'command':
                svc_dict['command'] = val
            elif key == 'entrypoint':
                svc_dict['entrypoint'] = val
            elif key == 'env':
                it = iter(val)
                svc_dict['environment'] = {k: v for k, v in zip(it, it)}
            elif key == 'env_file':
                svc_dict['env_file'] = [val]
            elif key == 'volume':
                vn = f"{svc.nome}_vol0"
                svc_dict.setdefault('volumes', []).append(f"{vn}:{val}")
                vols.add(vn)
            elif key == 'depends_on':
                svc_dict['depends_on'] = val
            elif key == 'networks':
                svc_dict['networks'] = val
                nets.update(val)
            elif key == 'labels':
                it = iter(val)
                svc_dict['labels'] = {k: v for k, v in zip(it, it)}
            elif key == 'extra_hosts':
                svc_dict['extra_hosts'] = val
            elif key == 'ulimits':
                svc_dict['ulimits'] = {r: l for r, l in val}

        doc['services'][svc.nome] = svc_dict

    # Seção volumes
    if vols:
        doc['volumes'] = {v: None for v in sorted(vols)}
    # Seção networks
    if nets:
        doc['networks'] = {n: None for n in sorted(nets)}

    # Escreve o arquivo com cabeçalho de comentários
    with open(output, 'w', encoding='utf-8') as f:
        f.write(
            "# 🚀 Docker Compose gerado pelo Dangui DSL\n"
            "# 🔧 Boas práticas:\n"
            "#   • Docker Engine ≥ 20.10.0\n"
            "#   • Docker Compose ≥ 1.29.0\n"
            "#   • Consulte https://docs.docker.com/compose/ para mais detalhes\n\n"
        )
        # Emite o YAML propriamente dito
        yaml.dump(doc, f, sort_keys=False, allow_unicode=True)

    print(f"✔️  '{output}' gerado com sucesso.")
