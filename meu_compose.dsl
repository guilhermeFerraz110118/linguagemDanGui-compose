# Serviço de proxy reverso com Traefik
serviço "proxy" {
  imagem "traefik:v2.9"
  reiniciar "always"
  comando ["--api.insecure=true","--providers.docker"]
  ponto_entrada ["--api.insecure=true","--providers.docker"]
  portas(80:80,443:443)
  redes("frontend","backend")
  rotulos("traefik.enable","true")
}

# Aplicação web em React (build local)
serviço "frontend" {
  construir "./frontend"
  argumentos("NODE_ENV","production")
  reiniciar "on-failure"
  portas(3000:3000)
  env("API_URL","http://proxy/api")
  redes("frontend")
}

# API em Python com Flask
serviço "api" {
  construir "./api"
  env("FLASK_ENV","production","DEBUG","False")
  arquivo_env ".env.api"
  comando ["flask","run","--host=0.0.0.0"]
  portas(5000:5000)
  dependentes("db")
  redes("backend")
}

# Worker Celery
serviço "worker" {
  imagem "python:3.10"
  comando ["celery","-A","tasks","worker","--loglevel=info"]
  env("BROKER_URL","redis://cache:6379/0")
  dependentes("cache")
  redes("backend")
}

# Banco de dados MySQL
serviço "db" {
  imagem "mysql:5.7"
  reiniciar "unless-stopped"
  env("MYSQL_ROOT_PASSWORD","root","MYSQL_DATABASE","appdb","MYSQL_USER","app","MYSQL_PASSWORD","secret")
  volume "/var/lib/mysql"
  redes("backend")
}

# Cache Redis
serviço "cache" {
  imagem "redis:6-alpine"
  reiniciar "always"
  expor(6379)
  redes("backend")
}

# phpMyAdmin para gerenciar o DB
serviço "db_admin" {
  imagem "phpmyadmin:5"
  reiniciar "always"
  portas(8080:80)
  env("PMA_HOST","db")
  hosts_extras("db:db.local")
  redes("backend")
}

# Monitoramento com Prometheus
serviço "prometheus" {
  imagem "prom/prometheus:v2.33.1"
  reiniciar "always"
  expor(9090)
  volume "/etc/prometheus"
  redes("monitoring")
}

# Alertas com Alertmanager
serviço "alertmanager" {
  imagem "prom/alertmanager:v0.23.0"
  reiniciar "always"
  portas(9093:9093)
  redes("monitoring")
}

# Grafana para dashboards
serviço "grafana" {
  imagem "grafana/grafana:8.5.2"
  reiniciar "always"
  portas(3001:3000)
  env("GF_SECURITY_ADMIN_PASSWORD","admin")
  redes("monitoring")
}

# Rede isolada para testes
serviço "test_net" {
  imagem "alpine"
  comando ["sleep","infinity"]
  redes("isolated")
}
