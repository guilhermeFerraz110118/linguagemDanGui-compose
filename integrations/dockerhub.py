import requests

class DockerHubError(Exception):
    """Erro ao consultar Docker Hub."""
    pass

def fetch_tags(repository: str, page_size: int = 50):
    """
    Busca no Docker Hub as tags de um repositório.
    repository: 'nginx' ou 'usuario/repositorio'
    Retorna lista de tags ['latest','1.21','1.20',...].
    """
    tags = []
    url = f"https://registry.hub.docker.com/v2/repositories/{repository}/tags"
    params = {'page_size': page_size}
    while url:
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code != 200:
            raise DockerHubError(f"Status {resp.status_code} ao buscar tags")
        data = resp.json()
        tags += [t['name'] for t in data.get('results', [])]
        url = data.get('next')
        params = {}
    return tags

# Especificações de variáveis de ambiente para imagens comuns
IMAGE_ENV_SPECS = {
    'mysql': {
        'required': ['MYSQL_ROOT_PASSWORD'],
        'optional': ['MYSQL_DATABASE','MYSQL_USER','MYSQL_PASSWORD']
    },
    'redis': {
        'required': [],
        'optional': ['REDIS_PASSWORD']
    },
    'nginx': {
        'required': [],
        'optional': []
    },
    'python': {
        'required': [],
        'optional': []
    },
    # adicione mais conforme necessário
}

def get_env_spec(image_tag: str):
    """
    Retorna spec de env vars para a imagem selecionada.
    image_tag: 'nome:tag'
    """
    base = image_tag.split(':', 1)[0]
    return IMAGE_ENV_SPECS.get(base)
