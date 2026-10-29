# Metodologia e governança analítica

## Princípios

- Fonte oficial e identificável.
- Separação entre dado original, dado tratado e interpretação.
- Granularidade e universo explicitados em cada métrica.
- Preservação de códigos oficiais e identificadores.
- Transformações versionadas e testadas.
- Resultados reproduzíveis a partir de parâmetros e fontes documentados.

## Granularidade

Toda tabela analítica deverá declarar a unidade de observação. Exemplos: candidato por eleição, votação por seção/cargo/candidato, eleitorado por município/faixa etária, receita por prestador/fornecedor e pesquisa por registro/período.

Não agregar ou relacionar tabelas sem verificar se as chaves e a granularidade são compatíveis. Uma junção muitos-para-muitos pode multiplicar registros e distorcer totais.

## Comparabilidade histórica

Leiautes, códigos, regras eleitorais, cargos e classificações podem mudar entre eleições. Comparações temporais exigem:
- documentação das versões dos leiautes;
- mapeamento explícito de categorias;
- identificação de alterações de fronteiras ou códigos;
- registro de campos sem correspondência;
- validação dos totais antes e depois da harmonização.

## Qualidade de dados

Os testes devem cobrir, conforme aplicável:
- presença de campos obrigatórios;
- tipo e formato;
- domínio de códigos;
- unicidade de chaves;
- integridade referencial;
- duplicidade;
- valores ausentes;
- reconciliação de totais;
- consistência temporal e geográfica.

Falhas devem ser reportadas; não corrigir silenciosamente valores da fonte.

## Interpretação responsável

Resultados eleitorais agregados descrevem registros e totais em determinada granularidade. Não identificam a escolha de um eleitor específico. Correlação, associação e variação temporal não demonstram causalidade por si só.

## Proveniência mínima

Toda saída analítica deve permitir recuperar:
- fonte, dataset ID e resource ID;
- URL e data de extração;
- checksum do arquivo de origem;
- versão do código e parâmetros;
- filtros e regras de transformação;
- data de processamento;
- resultados dos testes de qualidade.
