# Aplicação Streamlit

A aplicação em `apps/analytics` permite pesquisar e inspecionar os metadados do catálogo TSE gerado pelo coletor CKAN.

## Instalação e execução

```bash
python -m pip install -r apps/analytics/requirements.txt
python scripts/discover_tse_catalog.py
streamlit run apps/analytics/app.py
```

A aplicação não cria indicadores eleitorais a partir de metadados. Se o manifesto não existir, informa como gerar o catálogo e não apresenta números fictícios. A pesquisa é textual e a exportação CSV contém apenas os registros filtrados carregados do manifesto.
