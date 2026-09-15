"""
executar_todos.py

Roda o problema das N damas, usando Busca em Profundidade (aigyminsper),
para todos os tamanhos de tabuleiro pedidos no enunciado da APS 3:
4, 5, 6, 7 e 8. Valida cada solucao encontrada (confere se realmente
nenhuma dama ataca outra) e salva um resumo em resultados/resumo.csv.
"""

import csv

from NQueens import NQueensState, imprimir_tabuleiro, resolver_n_damas

TAMANHOS = [4, 5, 6, 7, 8]


def validar_solucao(colunas):
    """Confere que nenhuma dama ataca outra (mesma coluna ou diagonal).
    As linhas nunca se repetem por construcao (uma dama por linha)."""
    n = len(colunas)
    for i in range(n):
        for j in range(i + 1, n):
            mesma_coluna = colunas[i] == colunas[j]
            mesma_diagonal = abs(colunas[i] - colunas[j]) == abs(i - j)
            if mesma_coluna or mesma_diagonal:
                return False
    return True


def main():
    linhas_csv = []

    for n in TAMANHOS:
        resultado, tempo = resolver_n_damas(n, algoritmo="BP")

        if resultado is None:
            print(f"N={n}: nenhuma solucao encontrada ({tempo:.6f}s)")
            linhas_csv.append({"n": n, "solucao_valida": "N/A", "tempo_s": f"{tempo:.6f}",
                                "colunas": ""})
            continue

        colunas = resultado.state.colunas
        valida = validar_solucao(colunas)

        print(f"\n=== N = {n} (tempo: {tempo:.6f}s) ===")
        print(f"Solucao (coluna de cada linha): {colunas}")
        print(f"Solucao valida? {'SIM' if valida else 'NAO -- ERRO!'}")
        print(imprimir_tabuleiro(colunas, n))

        linhas_csv.append({
            "n": n,
            "solucao_valida": "sim" if valida else "NAO",
            "tempo_s": f"{tempo:.6f}",
            "colunas": str(colunas),
        })

    with open("resultados/resumo.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "solucao_valida", "tempo_s", "colunas"])
        writer.writeheader()
        writer.writerows(linhas_csv)

    print("\nResumo salvo em resultados/resumo.csv")


if __name__ == "__main__":
    main()
