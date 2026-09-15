# APS 3 - IA: Problema das N Damas com Busca em Profundidade (AIGYM)

Resolve o problema classico das N damas para tabuleiros de dimensao **4, 5, 6, 7 e 8**,
usando **Busca em Profundidade (BuscaProfundidade)** da biblioteca
[`aigyminsper`](https://insper.github.io/ai_gym/).

## Estrutura

```
NQueens.py         -> implementacao do estado (NQueensState) + resolucao de um N especifico
executar_todos.py  -> roda os 5 tamanhos pedidos (4..8), valida as solucoes e salva resumo.csv
resultados/resumo.csv -> tabela com tempo, solucao encontrada e validacao para cada N
```

## Modelagem do problema

- **Estado**: uma tupla `colunas`, onde `colunas[i]` e a coluna da dama posicionada na
  linha `i`. As damas sao colocadas uma linha por vez, sempre a partir da proxima linha
  livre (`len(colunas)`).
- **Sucessores**: para o proximo estado, so sao geradas damas em colunas **seguras**
  (sem conflito de coluna ou diagonal com as damas ja colocadas). Como cada dama fica em
  uma linha diferente, conflito de linha nunca acontece por construcao.
- **Estado objetivo**: quando as `n` damas ja foram posicionadas (`len(colunas) == n`).
- **Por que Busca em Profundidade funciona bem aqui**: como `successors()` ja descarta os
  ramos invalidos (colunas/diagonais em conflito), a BP se comporta exatamente como um
  backtracking classico: ela desce um ramo ate o fim, e so "volta" (pop da pilha) quando
  um estado nao tem mais sucessores seguros. Isso e bem mais eficiente do que gerar todas
  as N^n combinacoes possiveis e filtrar depois.
- **Limite de profundidade (m)**: `m = n`, pois nunca e necessario (nem possivel) colocar
  mais de uma dama por linha - o objetivo e atingido exatamente na profundidade `n`.

## Como rodar

```bash
pip install aigyminsper

# resolver um tamanho especifico (ex: 8 damas, com Busca em Profundidade)
python3 NQueens.py 8 BP

# rodar todos os tamanhos pedidos no enunciado (4, 5, 6, 7, 8) e validar as solucoes
python3 executar_todos.py
```

## Resultados

Todas as solucoes para N = 4, 5, 6, 7 e 8 foram encontradas em menos de 1 milissegundo
e validadas (nenhuma dama ataca outra). Ver `resultados/resumo.csv` para os detalhes
de cada execucao (tempo e posicionamento das damas).
