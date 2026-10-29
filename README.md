# Brasil Eleitoral DataLab

<p align="center">
  <strong>Engenharia de dados, catálogo público e análise reproduzível do ecossistema eleitoral brasileiro.</strong>
</p>

<p align="center">
  <a href="https://dadosabertos.tse.jus.br/">Dados Abertos do TSE</a> ·
  <a href="docs/architecture/overview.md">Arquitetura</a> ·
  <a href="catalog/sources/tse.yml">Catálogo de fontes</a> ·
  <a href="CONTRIBUTING.md">Contribuição</a> ·
  <a href="LICENSE">Licença MIT</a>
</p>

O Brasil Eleitoral DataLab é uma iniciativa independente para descobrir, documentar, integrar, validar e analisar dados públicos relacionados ao processo eleitoral brasileiro. O objetivo é oferecer um ponto de entrada técnico para pesquisadores, jornalistas, estudantes, desenvolvedores e cidadãos interessados em explorar dados eleitorais com rastreabilidade e reprodutibilidade.

O projeto não se limita à auditoria de urnas eletrônicas. Seu escopo abrange resultados eleitorais, candidaturas, eleitorado, partidos, financiamento de campanhas, pesquisas eleitorais, boletins de urna, arquivos técnicos de totalização, geografia eleitoral e documentação institucional.

> **Estado atual:** fundação documental, arquitetura inicial e catálogo de fontes implementados. Os domínios listados representam o escopo de descoberta; não significam que os dados já tenham sido baixados, tratados ou integrados. A situação de cada conjunto será registrada individualmente no catálogo.

## Escopo de dados

| Domínio | Exemplos de conteúdo | Fonte prioritária |
|---|---|---|
| Resultados eleitorais | Votação por cargo, candidato, partido, município, zona e seção | TSE |
| Candidaturas | Perfil, situação, partido, federação, bens e propostas | TSE |
| Eleitorado | Perfil agregado, comparecimento, abstenção e locais de votação | TSE |
| Urnas e totalização | Boletins de urna, RDV, logs e arquivos de totalização | TSE |
| Financiamento | Receitas, despesas, doadores, fornecedores e prestação de contas | TSE |
| Pesquisas | Registros, institutos, contratantes e resultados publicados | TSE |
| Partidos | Órgãos partidários e informações partidárias disponíveis | TSE |
| Geografia eleitoral | Municípios, zonas, seções e códigos de referência | TSE / IBGE |
| Contexto institucional | Legislação, normas, fiscalização e dados públicos correlatos | Órgãos oficiais |

A disponibilidade, a granularidade, o histórico e a periodicidade variam por conjunto. Cada integração deverá ser precedida pela leitura dos metadados e do dicionário oficial.

## Fontes e catálogo

A fonte primária é o [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/), que utiliza CKAN e disponibiliza catálogo de conjuntos e recursos. O portal substituiu o antigo Repositório de Dados Eleitorais.

- [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/)
- [Catálogo de conjuntos](https://dadosabertos.tse.jus.br/dataset/)
- [API CKAN — busca de conjuntos](https://dadosabertos.tse.jus.br/api/3/action/package_search)
- [TSE — Estatísticas eleitorais](https://www.tse.jus.br/eleicoes/estatisticas)

Fontes complementares, como IBGE e Dados.gov.br, serão adicionadas quando houver relação metodológica clara com os dados eleitorais.

O catálogo local fica em `catalog/`. Cada registro deverá informar identificador, órgão responsável, URL oficial, formatos, cobertura temporal e geográfica, granularidade, licença declarada pela fonte, frequência de atualização, data da verificação e situação da integração.

## Arquitetura

A solução será híbrida:

- **Web:** JavaScript / TypeScript com Next.js para navegação, catálogo e experiência pública.
- **API:** Node.js / TypeScript para expor metadados e serviços da aplicação.
- **Dados e pipelines:** Python para descoberta, download, extração, validação e transformação.
- **Exploração analítica:** Streamlit para aplicações de análise interativa.
- **Consulta e armazenamento analítico:** DuckDB e Parquet; PostgreSQL quando houver necessidade transacional ou de serviço compartilhado.

### Camadas de dados

| Camada | Responsabilidade |
|---|---|
| Landing / Bronze | Preservar arquivos originais, metadados, checksums e evidências de extração |
| Silver | Padronizar schemas, tipos, códigos e regras de qualidade sem perder proveniência |
| Gold | Publicar tabelas analíticas e indicadores com granularidade e metodologia explícitas |

A arquitetura detalhada e os limites entre componentes estão em [docs/architecture/overview.md](docs/architecture/overview.md).

## Princípios de engenharia e auditoria

1. **Proveniência:** toda tabela derivada deve apontar para a fonte, recurso, versão e execução que a originaram.
2. **Integridade:** registrar tamanho, checksum e resultado das verificações aplicáveis aos arquivos.
3. **Idempotência:** reprocessar a mesma versão não deve gerar duplicações silenciosas.
4. **Contratos de dados:** documentar schema, tipos, chaves, granularidade e semântica.
5. **Qualidade:** testar obrigatoriedade, domínio, duplicidade, integridade referencial e reconciliação de contagens.
6. **Reprodutibilidade:** registrar parâmetros, versões de código e datas de extração.
7. **Segurança:** tratar arquivos externos como não confiáveis; limitar extração de arquivos compactados e não versionar dados pessoais ou credenciais.
8. **Neutralidade analítica:** separar dado observado, hipótese e interpretação; não apresentar correlação como causalidade.

Dados eleitorais agregados não autorizam inferências sobre escolhas ou comportamentos individuais. A granularidade e as limitações de cada fonte devem acompanhar qualquer análise publicada.

## Estrutura do repositório

```text
brasil-eleitoral-datalab/
├── apps/
│   ├── web/                  # Next.js (JavaScript / TypeScript)
│   └── analytics/            # Streamlit (Python)
├── services/
│   └── api/                  # API Node.js / TypeScript
├── src/
│   └── brasil_eleitoral/
│       ├── catalog/
│       ├── ingestion/
│       ├── validation/
│       ├── transformation/
│       └── storage/
├── catalog/
│   ├── sources/
│   └── datasets/
├── docs/
│   ├── architecture/
│   ├── datasets/
│   ├── methodology/
│   └── tutorials/
├── examples/
├── notebooks/
├── scripts/
├── tests/
└── .github/workflows/
```

A estrutura será materializada incrementalmente. Diretórios ainda sem implementação não devem ser interpretados como componentes operacionais.

## Situação do desenvolvimento

Legenda: [x] concluído e publicado; [ ] ainda não implementado ou não validado.

### Fundação e governança
- [x] Definição do escopo multidomínio.
- [x] Definição da arquitetura híbrida e separação entre componentes.
- [x] Documentação inicial da arquitetura.
- [x] Princípios de qualidade, proveniência, segurança e metodologia.
- [x] Padrão inicial de metadados para conjuntos de dados.
- [x] Registro inicial da fonte oficial do TSE.
- [x] Configuração inicial do `.gitignore`.
- [x] Inclusão da licença MIT para o código e a documentação originais do projeto.

### Engenharia de dados
- [x] Cliente CKAN com paginação, descoberta e coleta automatizada de metadados (implementado; consulta real ainda depende de execução no ambiente).
- [x] Normalização de metadados e exportação local em JSON, com manifesto SHA-256 e checkpoint de retomada.
- [x] Pipeline de download com retomada por HTTP Range/ETag, SHA-256 e manifesto atômico (testes simulados; execução real pendente).
- [x] Extrator ZIP seguro com limites, validação de integridade e testes (CI validada).
- [x] Contratos de dados versionados e validações automatizadas (CI validada).
- [x] Pipeline inicial Bronze/Silver/Gold com hashes, metadados, normalização CSV e agregação por granularidade explícita (fixtures locais; Parquet/DuckDB pendentes).
- [x] Pipeline ponta a ponta validado com fixture normalizada local (ingestão, contrato, Silver e Gold); integração com recurso oficial real do TSE ainda pendente.

### Aplicações e operação
- [x] API Node.js / TypeScript com health checks e endpoints de leitura do catálogo (testes automatizados).
- [x] Interface web Next.js inicial, responsiva e integrada à API.
- [x] Aplicação Streamlit para pesquisa e exportação do catálogo local.
- [x] Testes automatizados do cliente e do catálogo CKAN (respostas simuladas).
- [x] Workflow de CI para executar a suíte de testes.
- [x] Documentação de instalação, execução e exemplos reproduzíveis para descoberta, downloads, extração, contratos e medallion.
- [x] Logs JSON estruturados, códigos de saída e tratamento de falhas no pipeline local; [ ] monitoramento gerenciado, alertas e observabilidade de produção.

Os itens marcados como concluídos correspondem somente ao que já está versionado no repositório. Itens planejados permanecem desmarcados até que exista implementação publicada e validação correspondente. Esta lista será atualizada a cada entrega.

## Como executar a descoberta CKAN

Requer Python 3.10 ou superior. Instale o projeto e execute o coletor:

```bash
python -m pip install -e ".[dev]"
python scripts/discover_tse_catalog.py
python scripts/download_tse_resources.py
python scripts/process_election_results.py --input examples/election-results-normalized.csv --contract contracts/tse/election-results.v1.json --output data --dimensions election_year state_code office
```

O comando consulta o catálogo público do TSE, percorre as páginas da API e grava um JSON por conjunto em `catalog/tse/datasets/`, além de `manifest.json` e checkpoint. Os arquivos gerados são locais e estão excluídos do Git para evitar commits de snapshots extensos e variáveis. Consulte [docs/ckan-discovery.md](docs/ckan-discovery.md), [docs/resource-downloads.md](docs/resource-downloads.md), [docs/safe-extraction.md](docs/safe-extraction.md), [docs/data-contracts.md](docs/data-contracts.md), [docs/medallion-pipeline.md](docs/medallion-pipeline.md), [docs/api.md](docs/api.md) e [docs/streamlit.md](docs/streamlit.md), [docs/operations.md](docs/operations.md) e [docs/api.md](docs/api.md) para opções, formatos e limitações dos componentes.

A descoberta CKAN e o downloader possuem testes automatizados com respostas simuladas e passam no workflow de CI. A disponibilidade real, o total atual de conjuntos e a conclusão de uma coleta integral de metadados/recursos ainda precisam ser confirmados executando os comandos contra o portal em ambiente com acesso à internet.

Não publique arquivos brutos volumosos no Git. Prefira manifests, metadados, amostras pequenas e dados derivados cuja redistribuição seja permitida pela fonte.

## Referências

- [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/)
- [Tribunal Superior Eleitoral](https://www.tse.jus.br/)
- [IBGE](https://www.ibge.gov.br/)
- [Portal Brasileiro de Dados Abertos](https://dados.gov.br/)
- [DataUrnas-BR — referência de organização e documentação](https://github.com/alissonlinneker/dataUrnas-br)

## Licença

Este projeto é distribuído sob a licença [MIT](LICENSE).

A licença MIT aplica-se ao código-fonte e à documentação original deste repositório. Ela não substitui nem altera as licenças, termos de uso, direitos de terceiros ou condições de redistribuição dos conjuntos de dados, arquivos, marcas e materiais obtidos de fontes externas. Antes de redistribuir qualquer dado, consulte os metadados e as condições publicados pelo órgão responsável.
