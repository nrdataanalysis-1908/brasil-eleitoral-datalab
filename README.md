# Brasil Eleitoral DataLab

**Engenharia de Dados, integração e auditoria reproduzível de dados eleitorais brasileiros.**

O Brasil Eleitoral DataLab é um projeto de engenharia de dados voltado à coleta, padronização, validação e análise de dados eleitorais públicos do Brasil. A proposta é construir uma base técnica rastreável, reproduzível e orientada por evidências, utilizando fontes oficiais e documentando as transformações aplicadas aos dados.

> **Status do projeto:** estrutura inicial. Este repositório ainda não contém pipelines de ingestão, modelos de dados, análises ou testes automatizados. Os componentes descritos abaixo representam o escopo planejado, não funcionalidades já implementadas.

## Objetivos

- Integrar conjuntos de dados eleitorais publicados por fontes oficiais.
- Preservar a origem, a versão e a data de referência de cada conjunto de dados.
- Padronizar schemas, tipos, códigos geográficos e identificadores eleitorais.
- Aplicar validações de qualidade, consistência e integridade.
- Disponibilizar dados tratados para consultas analíticas reproduzíveis.
- Documentar critérios, limitações e decisões metodológicas.

## Fontes de dados

A fonte primária prevista é o portal de Dados Abertos do Tribunal Superior Eleitoral (TSE):

- [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/)
- [Tribunal Superior Eleitoral](https://www.tse.jus.br/)

A seleção de datasets será feita a partir do catálogo oficial. Cada integração deverá registrar, no mínimo, o recurso de origem, URL ou identificador no catálogo, data de extração, período eleitoral, formato, versão disponível e checksum do arquivo, quando aplicável.

A cobertura efetiva dependerá da disponibilidade, do layout e da documentação de cada conjunto de dados.

## Arquitetura de dados proposta

O desenho lógico prevê três camadas:

| Camada | Responsabilidade |
|---|---|
| **Bronze** | Preservar os arquivos originais, metadados de extração e evidências de integridade. |
| **Silver** | Normalizar schemas, tipos, códigos, categorias e regras de qualidade, mantendo rastreabilidade até a origem. |
| **Gold** | Publicar tabelas e agregações analíticas documentadas, prontas para consultas e visualizações. |

### Fluxo lógico previsto

1. Descoberta de datasets no catálogo oficial.
2. Extração dos arquivos e metadados.
3. Verificação de integridade e registro de proveniência.
4. Ingestão da fonte na camada Bronze.
5. Normalização e validação na camada Silver.
6. Construção de tabelas analíticas na camada Gold.
7. Testes, documentação e publicação dos resultados.

## Stack tecnológica em avaliação

A seleção final será feita conforme os formatos e volumes reais das fontes:

- **Python:** ingestão, transformação, validação e automação.
- **Pandas / Polars:** processamento tabular, conforme o perfil de cada dataset.
- **Parquet:** armazenamento colunar para dados tratados.
- **DuckDB:** consultas analíticas locais e reprodutíveis.
- **SQL:** modelagem, transformação e validação.
- **GitHub Actions:** automação de testes e verificações de qualidade.

Nenhuma dessas integrações deve ser considerada implementada até existir código versionado e teste correspondente no repositório.

## Qualidade, auditoria e reprodutibilidade

As pipelines deverão contemplar:

- Validação de schema e tipos de dados.
- Verificação de campos obrigatórios, valores nulos e duplicidades.
- Integridade referencial entre tabelas relacionadas.
- Validação de domínios e códigos oficiais.
- Reconciliação de contagens entre origem e destino.
- Registro de logs, erros, duração e volume processado.
- Versionamento de parâmetros e regras de transformação.
- Testes automatizados para regras críticas.

As execuções deverão ser idempotentes sempre que possível: reprocessar a mesma fonte e versão não deverá gerar duplicação silenciosa nem alterar resultados sem justificativa documentada.

## Princípios metodológicos

Dados eleitorais exigem interpretação cuidadosa. O projeto adotará os seguintes princípios:

1. **Fonte verificável:** priorizar dados oficiais e registrar a referência utilizada.
2. **Separação entre fato e interpretação:** resultados descritivos não serão apresentados como explicações causais.
3. **Granularidade explícita:** toda métrica deverá informar período, unidade geográfica, cargo e universo considerado.
4. **Junções controladas:** relacionamentos deverão utilizar chaves oficiais e regras documentadas.
5. **Limites de inferência:** dados agregados por seção, município ou zona não permitem concluir automaticamente o comportamento individual de eleitores.
6. **Reprodutibilidade:** análises deverão informar fonte, filtros, parâmetros e transformações.

## Estrutura planejada

A estrutura abaixo é uma referência de organização futura; diretórios e módulos serão adicionados conforme cada etapa for implementada.

```text
brasil-eleitoral-datalab/
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── docs/
│   ├── architecture.md
│   ├── data-dictionary.md
│   └── methodology.md
├── notebooks/
├── src/
│   └── brasil_eleitoral/
│       ├── ingestion/
│       ├── validation/
│       ├── transformation/
│       └── analytics/
├── tests/
├── .github/
│   └── workflows/
├── .gitignore
├── pyproject.toml
└── README.md
```

Arquivos eleitorais brutos, bases derivadas volumosas, credenciais e dados pessoais não devem ser versionados no Git. O repositório deverá manter apenas código, documentação, metadados e amostras pequenas cuja publicação seja apropriada.

## Roadmap

- [ ] Mapear o catálogo do TSE e selecionar o primeiro conjunto de dados.
- [ ] Documentar layout, granularidade, chaves e regras do dataset escolhido.
- [ ] Implementar ingestão reproduzível com metadados e integridade.
- [ ] Implementar validações e testes automatizados.
- [ ] Estruturar as camadas Bronze, Silver e Gold.
- [ ] Disponibilizar consultas analíticas e exemplos reproduzíveis.
- [ ] Automatizar verificações com CI.

## Como contribuir

Contribuições devem preservar a rastreabilidade das fontes, incluir documentação das regras aplicadas e adicionar testes para transformações ou validações relevantes. Alterações metodológicas precisam explicitar seus impactos nos resultados.

## Licença

A licença do projeto ainda não foi definida. Até que uma licença seja adicionada ao repositório, não se deve presumir autorização para reutilização, redistribuição ou uso comercial do conteúdo.
