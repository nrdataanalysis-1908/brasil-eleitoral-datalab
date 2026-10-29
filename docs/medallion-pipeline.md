# Bronze, Silver e Gold

O módulo `brasil_eleitoral.transformation.medallion` implementa um pipeline local, reproduzível e sem dependências externas. Ele não presume que os arquivos oficiais do TSE compartilhem um único schema: a normalização de nomes e a granularidade analítica são explícitas.

## Bronze

`bronze_ingest(source, root, source_id, dataset, execution_id)` preserva o arquivo original sem transformação. O endereço é derivado do SHA-256 do conteúdo, tornando a gravação idempotente por conteúdo. Um JSON lateral registra fonte, nome original, tamanho, hash e execução. O arquivo armazenado não deve ser editado.

## Silver

`silver_normalize_csv(source, destination)` padroniza cabeçalhos para snake_case ASCII, remove espaços periféricos e mantém os valores como texto para evitar conversões sem dicionário oficial. Gera metadados com colunas, contagem de linhas e hashes de entrada/saída. Colunas que colidem após normalização causam erro.

## Gold

`gold_aggregate_results(source, destination, dimensions, metric="votes")` soma uma métrica numérica não negativa por dimensões explicitamente fornecidas. A granularidade do agregado é exatamente a tupla de dimensões informada. Valores ausentes nas dimensões ou métricas inválidas interrompem a publicação.

## Exemplo

```python
from pathlib import Path
from brasil_eleitoral.transformation import (
    bronze_ingest, silver_normalize_csv, gold_aggregate_results,
)

bronze_ingest(Path("results.csv"), Path("data"), source_id="tse",
              dataset="results_2022", execution_id="manual-001")
silver_normalize_csv(Path("results.csv"), Path("data/silver/results_2022.csv"))
gold_aggregate_results(Path("data/silver/results_2022.csv"),
                       Path("data/gold/votes_by_state.csv"),
                       dimensions=("state_code", "office"), metric="votes")
```

O exemplo requer que o CSV de entrada contenha as colunas indicadas. Não é uma afirmação de que todo arquivo TSE já possua esse layout. O mapeamento do layout oficial para o schema normalizado deve ser documentado por conjunto e validado com o contrato correspondente.

## Limites

A implementação atual publica CSV nas camadas Silver/Gold e mantém os originais na Bronze. Parquet/DuckDB, particionamento de grande volume, orquestração distribuída e integração validada com um recurso real do TSE permanecem etapas separadas. Os testes usam fixtures locais; não comprovam download ou processamento live do TSE.
