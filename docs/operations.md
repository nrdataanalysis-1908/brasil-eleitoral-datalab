# Operação e observabilidade

O módulo `brasil_eleitoral.observability` emite eventos JSON em stdout com timestamp UTC, nível, logger, evento e atributos operacionais conhecidos. Erros incluem stack trace. Não registrar conteúdo eleitoral sensível, tokens ou credenciais.

## Pipeline local integrado

O script `scripts/process_election_results.py` encadeia preservação Bronze, validação pelo contrato JSON, normalização Silver e agregação Gold. Ele exige um CSV previamente mapeado para o schema declarado; não tenta adivinhar o layout de arquivos oficiais do TSE.

```bash
python scripts/process_election_results.py \
  --input examples/election-results-normalized.csv \
  --contract contracts/tse/election-results.v1.json \
  --output data \
  --dimensions election_year state_code office
```

O comando retorna código 0 em sucesso, 2 em falha de contrato e 1 em falha operacional. Cada camada registra hashes e metadados. Para produção, encaminhe stdout/stderr para a plataforma de logs do ambiente e configure alertas externos para falhas; este repositório ainda não provisiona serviço de monitoramento gerenciado.

A execução com fixtures é reprodutível localmente. A integração ponta a ponta com um recurso oficial real do TSE depende de mapear seu dicionário de dados, obter o arquivo em ambiente com internet e executar o pipeline contra ele.
