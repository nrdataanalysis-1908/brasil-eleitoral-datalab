# Ambiente local integrado

O projeto oferece uma composição Docker para executar API, interface web e aplicação Streamlit em conjunto.

## Requisitos

Docker Engine e Docker Compose v2.

## Inicialização

```bash
docker compose up --build
```

Serviços:

- Web: http://localhost:3000
- API: http://localhost:3001/health
- Streamlit: http://localhost:8501

O diretório catalog é montado como somente leitura nos serviços que consultam metadados. Gere o catálogo no host antes de subir a stack, usando um ambiente com acesso à internet. O compose é uma configuração de desenvolvimento; não substitui proxy TLS, autenticação, gestão de segredos, limites de recursos, backups ou hardening de produção.

Para encerrar: `docker compose down`.
