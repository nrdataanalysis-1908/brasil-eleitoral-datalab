# Brasil Eleitoral DataLab

Plataforma de engenharia, auditoria e análise de dados eleitorais brasileiros, com foco em dados públicos, rastreabilidade e processamento reproduzível.

<p>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Node.js-20%2B-339933?logo=nodedotjs&logoColor=white" alt="Node.js">
  <img src="https://img.shields.io/badge/Next.js-Web-000000?logo=nextdotjs" alt="Next.js">
  <img src="https://img.shields.io/badge/Streamlit-Analytics-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Plotly-Charts-3F4F75?logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/Source-TSE-0B6E99" alt="TSE">
</p>

---

## Sobre

O Brasil Eleitoral DataLab organiza diferentes conjuntos públicos do ecossistema eleitoral em um fluxo técnico único: descoberta de fontes, ingestão de arquivos, validação, transformação e exploração analítica.

O projeto toma como referência de documentação e apresentação o [DataUrnas-BR](https://github.com/alissonlinneker/dataUrnas-BR), mas possui escopo e implementação próprios. Enquanto a referência é centrada em auditoria de arquivos de urna, este laboratório busca integrar diferentes domínios eleitorais e oferecer uma base extensível para análises reproduzíveis.

## O que o projeto reúne

| Módulo | Responsabilidade | Tecnologia |
|---|---|---|
| Descoberta | Consulta e catalogação dos conjuntos publicados pelo TSE | Python / CKAN |
| Ingestão | Download resiliente, retomada e verificação de integridade | Python |
| Qualidade | Contratos, schema, tipos, chaves e regras de validação | Python |
| Transformação | Organização dos dados em Bronze, Silver e Gold | Python |
| API | Exposição de catálogo e verificações de serviço | Node.js |
| Aplicação web | Navegação e visualização geral do projeto | Next.js |
| Analytics | Exploração, filtros, gráficos e exportação | Streamlit / Plotly |

## Painel analítico

O Streamlit explora os metadados coletados no catálogo CKAN do TSE. Inclui:

- distribuição de recursos por formato;
- quantidade de conjuntos por órgão;
- conjuntos criados por ano;
- atualizações do catálogo ao longo do tempo;
- conjuntos com maior número de recursos;
- filtros por órgão, formato e texto;
- tabela de consulta e exportação CSV.

> Os gráficos disponíveis nesta etapa representam a estrutura e os metadados do catálogo. Não representam votos, candidatos, comparecimento ou abstenção. Indicadores eleitorais só serão apresentados após ingestão e validação dos arquivos oficiais correspondentes.

## Arquitetura

    TSE / CKAN / outras fontes públicas
                   |
                   v
          Descoberta de dados
                   |
                   v
       Download e extração segura
                   |
                   v
        Validação por contratos
                   |
                   v
          Bronze -> Silver -> Gold
                   |
             +-----+------+
             |            |
             v            v
          Node API    Dados analíticos
             |         (evolução)
             v            |
          Next.js      Streamlit
           Web UI     Plotly Analytics

### Camadas de dados

- Bronze: arquivos originais, metadados de origem, hashes e evidências de ingestão.
- Silver: dados normalizados, tipados e submetidos às regras de qualidade.
- Gold: tabelas analíticas com granularidade e semântica documentadas.

## Pipeline de dados

1. Descoberta de conjuntos e recursos no catálogo CKAN do TSE.
2. Geração de manifesto, hash SHA-256 e checkpoint.
3. Download com streaming, retry/backoff e retomada HTTP Range/ETag.
4. Extração ZIP com validação de caminhos, limites e CRC.
5. Validação de registros por contratos versionados.
6. Transformação inicial Bronze/Silver/Gold com dados de teste normalizados.
7. Consulta por API e interfaces de exploração.

Os componentes de ingestão e transformação possuem testes automatizados com fixtures. A execução integral contra os arquivos reais do TSE ainda precisa ser realizada e validada em ambiente com acesso à fonte.

## Fontes de dados no escopo

| Domínio | Exemplos |
|---|---|
| Resultados | Votos por cargo, candidatura, partido, município, zona e seção |
| Candidaturas | Situação, partido, federação, bens e propostas |
| Eleitorado | Perfil agregado, comparecimento, abstenção e locais |
| Urnas e totalização | Boletins de urna, logs, RDV e arquivos de totalização |
| Financiamento | Receitas, despesas, doadores e fornecedores |
| Pesquisas | Registros, institutos, contratantes e resultados publicados |
| Geografia | Municípios, zonas, seções e códigos geográficos |

A presença de um domínio nesta tabela indica escopo planejado, não integração concluída.

## Como executar

### Requisitos

- Python 3.10 ou superior
- Node.js 20 ou superior
- Docker Compose (opcional)

### 1. Clonar e instalar

    git clone https://github.com/nrdataanalysis-1908/brasil-eleitoral-datalab.git
    cd brasil-eleitoral-datalab
    python -m venv .venv

Linux/macOS:

    source .venv/bin/activate

Windows PowerShell:

    .venv\Scripts\Activate.ps1

Instalar dependências:

    python -m pip install -e ".[dev]"

### 2. Descobrir o catálogo do TSE

    python scripts/discover_tse_catalog.py

A descoberta requer acesso à internet. O processo gera os metadados e o manifesto local em catalog/tse/datasets/.

### 3. Abrir o painel Streamlit

    python -m pip install -r apps/analytics/requirements.txt
    streamlit run apps/analytics/app.py

O painel utiliza o manifesto gerado na etapa de descoberta. Se ele ainda não existir, a aplicação informa como gerá-lo; não utiliza dados fictícios.

### 4. Subir os serviços com Docker

    docker compose up --build

Consulte docs/development-stack.md para detalhes da stack local.

## Estrutura do repositório

    brasil-eleitoral-datalab/
    ├── apps/
    │   ├── web/                  # Next.js / TypeScript
    │   └── analytics/            # Streamlit / Plotly
    ├── services/
    │   └── api/                  # API Node.js
    ├── src/brasil_eleitoral/
    │   ├── ckan/                 # Cliente e catálogo CKAN
    │   ├── ingestion/            # Download e extração
    │   ├── validation/           # Contratos e qualidade
    │   ├── transformation/       # Bronze / Silver / Gold
    │   └── observability.py      # Logs estruturados
    ├── contracts/                # Contratos versionados
    ├── catalog/                  # Manifestos e metadados locais
    ├── docs/                     # Documentação técnica
    ├── examples/                 # Fixtures de referência
    ├── scripts/                  # Entradas de execução
    └── tests/                    # Testes automatizados

## Estado de desenvolvimento

| Componente | Situação |
|---|---|
| Cliente CKAN, paginação e descoberta | Implementado; execução real pendente |
| Manifesto, SHA-256 e checkpoint | Implementado |
| Download com retomada Range/ETag | Implementado; validação com fonte real pendente |
| Extração ZIP segura | Implementado e testado |
| Contratos e validação de dados | Implementado e testado |
| Pipeline Bronze/Silver/Gold | Implementação inicial com fixtures |
| API de catálogo | Implementada; validação final da suíte pendente |
| Web Next.js | Interface inicial |
| Streamlit / Plotly | Gráficos de metadados implementados |
| Ingestão integral de dados reais do TSE | Pendente |
| Indicadores eleitorais Gold e mapas por UF | Pendente |
| DuckDB / Parquet em produção | Pendente |
| Monitoramento gerenciado | Pendente |

## Documentação técnica

- [Fontes e catálogo de dados](docs/data-sources.md)
- [Descoberta CKAN](docs/ckan-discovery.md)
- [Download de recursos](docs/resource-downloads.md)
- [Extração segura](docs/safe-extraction.md)
- [Contratos de dados](docs/data-contracts.md)
- [Pipeline Medallion](docs/medallion-pipeline.md)
- [Operação e observabilidade](docs/operations.md)
- [Stack de desenvolvimento](docs/development-stack.md)
- [Aplicação Streamlit](docs/streamlit.md)

## Fontes oficiais

- [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/)
- [API CKAN do TSE](https://dadosabertos.tse.jus.br/api/3/action/package_search)
- [Estatísticas eleitorais do TSE](https://www.tse.jus.br/eleicoes/estatisticas)
- [IBGE](https://www.ibge.gov.br/)
- [Portal Brasileiro de Dados Abertos](https://dados.gov.br/)

## Princípios

- Rastreabilidade da origem à camada analítica.
- Integridade por hash, checksum e validação de schema.
- Processamento idempotente e reprodutível.
- Separação entre dado observado, interpretação e hipótese.
- Transparência sobre cobertura, limitações e etapas ainda não concluídas.
- Uso de dados agregados sem inferir escolhas ou comportamentos individuais.

## Licença

O código original deste repositório é distribuído sob a licença MIT. Os conjuntos de dados de terceiros permanecem sujeitos às licenças e condições definidas por seus respectivos órgãos publicadores.
