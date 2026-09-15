"""
NQueens.py

APS 3 - Problema das N Damas, resolvido com Busca em Profundidade (BP)
usando a biblioteca AIGYM (aigyminsper): https://insper.github.io/ai_gym/

O problema classico das N damas consiste em posicionar N damas em um
tabuleiro N x N de forma que nenhuma dama ataque outra (nenhuma duas
damas podem estar na mesma linha, mesma coluna ou mesma diagonal).

Representacao do estado
------------------------
Cada estado representa uma solucao PARCIAL do tabuleiro: uma tupla
`colunas` onde `colunas[i]` e a coluna da dama posicionada na linha `i`.
Ou seja, o estado com `colunas = (1, 3)` significa: ha uma dama na
linha 0 coluna 1, e uma dama na linha 1 coluna 3. As damas sao
posicionadas uma linha por vez, sempre da linha `len(colunas)` em diante.

Geracao de sucessores
----------------------
A cada estado, so sao gerados sucessores que colocam uma dama SEGURA
(sem conflito com as damas ja posicionadas) na proxima linha livre.
Isso significa que o proprio successors() ja faz a poda dos ramos
invalidos, exatamente como um backtracking classico - por isso a Busca
em Profundidade (que usa uma pilha, explorando um ramo ate o fim antes
de voltar) e uma escolha natural e eficiente para este problema: ela
so "backtracka" (volta a pilha) quando um ramo nao tem mais sucessores
seguros, e encontra a primeira solucao completa (goal) ao atingir a
linha N sem conflitos.

O limite de profundidade `m` da Busca em Profundidade e, portanto,
exatamente N (uma dama por linha - nunca e necessario, nem possivel,
descer mais do que N niveis).
"""

import sys
import time

from aigyminsper.search.graph import State
from aigyminsper.search.search_algorithms import BuscaLargura, BuscaProfundidade


class NQueensState(State):
    """Estado do problema das N damas: posicionamento parcial/completo
    de damas, uma por linha, representado por uma tupla de colunas."""

    def __init__(self, colunas, n, op):
        """
        colunas: tupla com a coluna de cada dama ja posicionada
                 (colunas[i] = coluna da dama na linha i)
        n: dimensao do tabuleiro (n x n, n damas)
        op: operador (acao) que gerou este estado
        """
        super().__init__(op)
        self.colunas = colunas
        self.n = n

    def _posicao_segura(self, coluna):
        """Verifica se colocar uma dama na proxima linha livre, na
        coluna informada, gera conflito com as damas ja posicionadas
        (mesma coluna ou mesma diagonal). Linhas repetidas nunca
        acontecem pois cada dama ja fica em uma linha distinta."""
        linha_nova = len(self.colunas)
        for linha_existente, coluna_existente in enumerate(self.colunas):
            mesma_coluna = coluna_existente == coluna
            mesma_diagonal = abs(coluna_existente - coluna) == abs(linha_existente - linha_nova)
            if mesma_coluna or mesma_diagonal:
                return False
        return True

    def successors(self):
        sucessores = []
        linha = len(self.colunas)

        # se ja posicionamos as N damas, nao ha mais sucessores (e estado objetivo)
        if linha >= self.n:
            return sucessores

        for coluna in range(self.n):
            if self._posicao_segura(coluna):
                novas_colunas = self.colunas + (coluna,)
                operador = f"linha{linha}=coluna{coluna}"
                sucessores.append(NQueensState(novas_colunas, self.n, operador))

        return sucessores

    def is_goal(self):
        return len(self.colunas) == self.n

    def description(self):
        return f"Problema das {self.n} damas (tabuleiro {self.n}x{self.n})"

    def cost(self):
        return 1

    def env(self):
        return f"{self.n}:{self.colunas}"


def imprimir_tabuleiro(colunas, n):
    """Imprime uma representacao visual do tabuleiro com as damas (Q)."""
    linhas = []
    for linha in range(n):
        casas = []
        for coluna in range(n):
            casas.append("Q" if colunas[linha] == coluna else ".")
        linhas.append(" ".join(casas))
    return "\n".join(linhas)


def resolver_n_damas(n, algoritmo="BP", pruning="without"):
    """
    Resolve o problema das N damas para um tabuleiro n x n.

    algoritmo: "BP" (Busca em Profundidade, com limite m=n) ou
               "BL" (Busca em Largura, sem limite de profundidade)
    """
    estado_inicial = NQueensState((), n, "")

    if algoritmo == "BL":
        busca = BuscaLargura()
        t0 = time.perf_counter()
        resultado = busca.search(estado_inicial, pruning=pruning)
        t1 = time.perf_counter()
    else:
        busca = BuscaProfundidade()
        t0 = time.perf_counter()
        resultado = busca.search(estado_inicial, m=n, pruning=pruning)
        t1 = time.perf_counter()

    tempo = t1 - t0
    return resultado, tempo


def main(n, algoritmo="BP"):
    print(f"\n=== Problema das {n} damas (algoritmo: {algoritmo}) ===")
    resultado, tempo = resolver_n_damas(n, algoritmo=algoritmo)

    if resultado is not None:
        colunas = resultado.state.colunas
        print(f"Solucao encontrada em {tempo:.6f}s: colunas = {colunas}")
        print(imprimir_tabuleiro(colunas, n))
    else:
        print(f"Nao ha solucao (tempo: {tempo:.6f}s)")

    return resultado, tempo


if __name__ == "__main__":
    n_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    algoritmo_arg = sys.argv[2] if len(sys.argv) > 2 else "BP"
    main(n_arg, algoritmo_arg)
