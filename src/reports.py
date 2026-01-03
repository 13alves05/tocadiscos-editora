"""
Cálculo dos direitos editoriais.

- Calcula receitas por autor com base nos álbuns vendidos
- Aplica percentagem de direitos
- Restringe acesso com autenticação
- Mostra relatório formatado com tabulate
"""

from tabulate import tabulate
from crud import load_autores, load_albuns
import management


def calcular_direitos_por_autor(autor):
    """
    Calcula estatísticas de um autor:
    - número de álbuns
    - unidades vendidas
    - receita total
    - direitos editoriais
    """

    todos_albuns = load_albuns()

    # Filtra apenas os álbuns do autor atual
    albuns_autor = [
        alb for alb in todos_albuns.values()
        if alb["artist_name"].lower() == autor["artist_name"].lower()
    ]

    num_albuns = len(albuns_autor)

    unidades_total = sum(int(alb["unites_sold"]) for alb in albuns_autor)

    receita_total = sum(
        int(alb["unites_sold"]) * float(alb["album_price"])
        for alb in albuns_autor
    )

    direitos_total = receita_total * (float(autor["rights_percentage"]) / 100)

    return {
        "num_albuns": num_albuns,
        "unidades_total": unidades_total,
        "receita_total": receita_total,
        "direitos_total": direitos_total
    }


def gerar_relatorio(ordenar_por="autor"):
    """
    Gera relatório financeiro dos direitos editoriais.
    Acesso restrito por palavra-passe.
    """

    # Verificação de acesso
    if not management.realizar_login():
        print("\nAcesso negado ao relatório. Palavra-passe incorreta.")
        return ""

    autores = load_autores()
    linhas = []

    total_albuns = 0
    total_unidades = 0
    total_receita = 0.0
    total_direitos = 0.0

    for autor in autores.values():
        calc = calcular_direitos_por_autor(autor)

        linhas.append([
            autor["artist_name"],
            autor["rights_percentage"],
            calc["num_albuns"],
            calc["unidades_total"],
            calc["receita_total"],
            calc["direitos_total"]
        ])

        total_albuns += calc["num_albuns"]
        total_unidades += calc["unidades_total"]
        total_receita += calc["receita_total"]
        total_direitos += calc["direitos_total"]

    # Ordenação
    if ordenar_por == "receita":
        linhas.sort(key=lambda x: x[4], reverse=True)
    else:
        linhas.sort(key=lambda x: x[0])

    # Linha de totais
    linhas.append([
        "TOTAL",
        "",
        total_albuns,
        total_unidades,
        total_receita,
        total_direitos
    ])

    # Formatação para apresentação
    formatadas = [
        [
            l[0],
            f"{l[1]:.1f}%" if isinstance(l[1], (int, float)) else l[1],
            l[2],
            l[3],
            f"{l[4]:.2f}€",
            f"{l[5]:.2f}€"
        ]
        for l in linhas
    ]

    cabecalhos = [
        "Autor",
        "% Direitos",
        "Nº Álbuns",
        "Unid. Vendidas",
        "Receita (€)",
        "Direitos (€)"
    ]

    print("\n" + "=" * 100)
    print("RELATÓRIO DE DIREITOS EDITORIAIS".center(100))
    print("=" * 100)
    print(tabulate(formatadas, cabecalhos, tablefmt="grid"))
    print("=" * 100)

    return tabulate(formatadas, cabecalhos, tablefmt="grid")