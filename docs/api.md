# API Node.js

API HTTP de leitura, implementada com módulos nativos do Node.js (sem dependências de runtime).

## Executar

```bash
cd services/api
node src/server.js
```

Porta padrão: `3001`; pode ser alterada pela variável `PORT`.

## Endpoints

- `GET /health`: estado do processo.
- `GET /api/v1/health`: health check versionado.
- `GET /api/v1/source`: conteúdo YAML da fonte TSE catalogada no repositório.
- `GET /api/v1/catalog`: manifesto local da descoberta CKAN, quando disponível. Sem manifesto, retorna `generated: false` e instrução para executar a descoberta.

Métodos diferentes de GET retornam 405; caminhos desconhecidos retornam 404. A API não afirma que o catálogo está atualizado sem uma execução local de descoberta. Autenticação, paginação pública, filtros e persistência PostgreSQL ainda não fazem parte desta primeira versão.
