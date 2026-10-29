# Arquitetura do Brasil Eleitoral DataLab

## 1. Objetivo

Construir uma plataforma reproduzível para descoberta, ingestão, validação, padronização e exploração de dados eleitorais públicos. A solução é híbrida: TypeScript atende a experiência web e serviços de aplicação; Python atende engenharia de dados e exploração Streamlit.

## 2. Componentes e responsabilidades

| Componente | Tecnologia | Responsabilidade |
|---|---|---|
| Web | Next.js / TypeScript | Navegação, busca, páginas de datasets e documentação |
| API | Node.js / TypeScript | Consultas ao catálogo interno e contratos HTTP |
| Data engineering | Python | Descoberta CKAN, download, extração, validação e transformação |
| Analytics | Streamlit / Python | Exploração interativa e protótipos analíticos |
| Analytical query | DuckDB | Consulta local de CSV e Parquet |
| Analytical storage | Parquet | Persistência colunar das camadas tratadas |
| Shared metadata | PostgreSQL (quando necessário) | Metadados operacionais e estado compartilhado |

Streamlit é uma aplicação Python. Componentes customizados podem incorporar tecnologias web, mas a aplicação Streamlit não será tratada como runtime JavaScript.

## 3. Integração com o TSE

O Portal de Dados Abertos do TSE utiliza CKAN. A descoberta deve consumir a API de ações CKAN, começando por `package_search`, e detalhar conjuntos e recursos por seus identificadores oficiais.

Endpoints-base:
- Catálogo: `https://dadosabertos.tse.jus.br/`
- API: `https://dadosabertos.tse.jus.br/api/3/action/`
- Busca: `package_search`
- Detalhe de conjunto: `package_show`
- Detalhe de recurso: `resource_show`

A resposta da API é a referência para o estado corrente do catálogo. Contagens de conjuntos, nomes de recursos, formatos e URLs não devem ser codificados como constantes permanentes.

## 4. Fluxo de dados

1. Descobrir conjuntos no catálogo CKAN.
2. Registrar metadados e IDs oficiais no catálogo local.
3. Inspecionar recursos, formatos, documentação e licença.
4. Baixar recursos com timeout, retry limitado e escrita temporária.
5. Verificar tamanho e SHA-256; preservar manifesto de ingestão.
6. Armazenar o arquivo original na camada Bronze.
7. Validar schema, codificação, delimitadores, chaves e domínios.
8. Normalizar para Silver, mantendo colunas de proveniência.
9. Publicar tabelas Gold com granularidade e metodologia documentadas.
10. Expor metadados e análises por API, web e Streamlit.

## 5. Camadas

### Landing / Bronze
- Arquivo original sem alteração.
- Metadados da fonte e do recurso.
- Data/hora de descoberta e download em UTC.
- URL de origem, tamanho, checksum e versão.
- Manifesto e logs da execução.

### Silver
- Tipos e nomes normalizados.
- Códigos oficiais preservados como strings quando houver zeros à esquerda.
- Regras de qualidade aplicadas e resultados registrados.
- Linhagem até arquivo e recurso de origem.

### Gold
- Fatos e dimensões analíticas.
- Agregações com unidade, período e filtros explícitos.
- Métricas documentadas e reprodutíveis.

## 6. Contrato mínimo de dataset

Cada registro deve conter: identificador interno, identificador CKAN, título, descrição, fonte, URL oficial, domínio, cobertura temporal e geográfica, granularidade, recursos, formatos, dicionário, licença, periodicidade, última verificação, estado de integração, checksums e limitações conhecidas.

O modelo inicial está em `catalog/datasets/_template.yml`.

## 7. Confiabilidade e segurança

- Idempotência por ID de recurso e checksum.
- Download para arquivo temporário e promoção atômica após validação.
- Retry com backoff limitado para falhas transitórias.
- Limites de tamanho, quantidade de entradas e razão de compressão em arquivos compactados.
- Rejeição de path traversal, links simbólicos e arquivos especiais na extração ZIP.
- Logs estruturados e manifesto por execução.
- Nunca executar conteúdo baixado.
- Não versionar credenciais, dados pessoais desnecessários ou grandes arquivos brutos.
- Verificar licença e termos por conjunto antes de redistribuir.

## 8. Observabilidade

Registrar ao menos: execução, dataset/resource ID, início e fim, status, bytes baixados, checksum, quantidade de registros quando calculável, duração, tentativas, erro e versão do código.

## 9. Limites de interpretação

A existência de um arquivo no portal não significa que ele esteja integrado ou validado neste projeto. A cobertura deve ser declarada por dataset e recurso. Análises agregadas não permitem inferir escolhas individuais nem estabelecer causalidade sem desenho metodológico apropriado.
