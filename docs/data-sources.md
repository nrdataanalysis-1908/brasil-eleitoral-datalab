# Fontes de dados

## Fonte primária: Tribunal Superior Eleitoral

O [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/) é a fonte prioritária para informações produzidas ou custodiadas pela Justiça Eleitoral. O portal substituiu o antigo Repositório de Dados Eleitorais.

O portal organiza informações em conjuntos de dados e recursos. Um conjunto pode conter múltiplos arquivos, anos, turnos, unidades federativas ou formatos. Por isso, o catálogo do projeto deve registrar os recursos individualmente, não apenas o título do conjunto.

### Descoberta via CKAN

Base da API:

```text
https://dadosabertos.tse.jus.br/api/3/action/
```

Ações utilizadas pelo desenho inicial:

- `package_search`: descobrir conjuntos e paginar resultados.
- `package_show`: recuperar metadados completos de um conjunto.
- `resource_show`: recuperar metadados de um recurso.

Exemplo de consulta HTTP:

```bash
curl --fail --silent --show-error \
  'https://dadosabertos.tse.jus.br/api/3/action/package_search?q=*:*&rows=10'
```

A API retorna um envelope CKAN com `success` e `result`. O consumidor deve validar `success`, tratar paginação e não presumir que a contagem de resultados seja constante.

### Domínios para descoberta

| Domínio interno | Temas encontrados no portal |
|---|---|
| `results` | Resultados, boletins de urna, logs e arquivos de totalização |
| `candidacies` | Candidatos, bens, propostas e situação |
| `electorate` | Perfil, locais de votação, comparecimento e abstenção |
| `campaign_finance` | Receitas, despesas e prestação de contas |
| `polls` | Pesquisas eleitorais registradas |
| `parties` | Órgãos e dados partidários |
| `electoral_processes` | Dados processuais eleitorais |
| `electoral_support` | Dados de apoio e infraestrutura eleitoral |

Os nomes acima são categorias internas do DataLab, não necessariamente nomes literais de grupos CKAN.

## Fontes complementares planejadas

| Fonte | Uso potencial | Regra |
|---|---|---|
| [IBGE](https://www.ibge.gov.br/) | Códigos e referências territoriais | Registrar versão e compatibilidade territorial |
| [Dados.gov.br](https://dados.gov.br/) | Descoberta federada de bases públicas | Evitar duplicar a fonte primária sem necessidade |
| [Câmara dos Deputados](https://www.camara.leg.br/) | Dados legislativos e institucionais | Integrar somente com caso de uso definido |
| [Senado Federal](https://www12.senado.leg.br/) | Dados legislativos e institucionais | Registrar endpoint e documentação oficial |

## Política de verificação

Antes de classificar um dataset como disponível ou integrado:

1. Abrir a página oficial do conjunto.
2. Consultar os metadados CKAN.
3. Enumerar recursos e formatos.
4. Ler o dicionário ou leiaute oficial.
5. Verificar licença, cobertura e atualização.
6. Registrar data da verificação e limitações.
7. Só então planejar e executar a ingestão.

Não presumir que todos os datasets possuam licença, periodicidade ou granularidade uniformes.


## Coletor implementado

O coletor inicial está disponível em `scripts/discover_tse_catalog.py`. Ele usa `package_search` com paginação, preserva metadados de conjuntos e recursos, grava arquivos JSON por conjunto e mantém manifesto/checkpoint com gravação atômica. A execução e as opções estão documentadas em [docs/ckan-discovery.md](ckan-discovery.md). A suíte automatizada cobre paginação, retomada, normalização, validação de slug e retry HTTP usando respostas simuladas; isso não substitui uma execução de integração contra o portal real.
