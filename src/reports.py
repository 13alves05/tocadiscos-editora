"""
Relatórios de Direitos Editoriais
- Calcula receitas por autor com base nos álbuns vendidos
- Aplica percentagem de direitos
- Restringe acesso com autenticação
- Mostra relatório formatado com alinhamento manual (como listar_autores)
"""

import management
from crud import autores, albuns  # Assume globals autores and albuns are loaded

def calcular_direitos_por_autor(nome_autor: str):
    """
    Calcula estatísticas de um autor: número de álbuns, unidades vendidas, receita total, direitos.
    """
    autor_albuns = [
        alb for alb in albuns.values()
        if alb["artist_name"].lower() == nome_autor.lower()
    ]

    num_albuns = len(autor_albuns)
    unidades_total = sum(int(alb.get("unites_sold", 0)) for alb in autor_albuns)
    receita_total = sum(
        int(alb.get("unites_sold", 0)) * float(alb.get("album_price", 0.0))
        for alb in autor_albuns
    )

    autor_rights_percentage = 0
    for autor_data in autores.values():
        if autor_data['artist_name'].lower() == nome_autor.lower():
            autor_rights_percentage = autor_data["rights_percentage"]
            break

    direitos_total = receita_total * (float(autor_rights_percentage) / 100)

    return {
        "num_albuns": num_albuns,
        "unidades_total": unidades_total,
        "receita_total": receita_total,
        "direitos_total": direitos_total
    }


def gerar_relatorio(ordenar_por="autor"):
    """
    Gera relatório financeiro dos direitos editoriais para todos os autores.
    Acesso restrito por palavra-passe.
    """
    # Verificação de acesso
    if not management.realizar_login():
        print("\nAcesso negado ao relatório. Palavra-passe incorreta.")
        return ""

    linhas = []
    total_albuns = 0
    total_unidades = 0
    total_receita = 0.0
    total_direitos = 0.0

    for autor_id, autor_data in autores.items():
        nome = autor_data.get("artist_name", "N/A").strip()
        percentagem = autor_data.get("rights_percentage", 0)

        calc = calcular_direitos_por_autor(nome)

        linhas.append([
            nome,
            f"{percentagem:.1f}%",
            calc["num_albuns"],
            calc["unidades_total"],
            f"{calc['receita_total']:.2f}€",
            f"{calc['direitos_total']:.2f}€"
        ])

        total_albuns += calc["num_albuns"]
        total_unidades += calc["unidades_total"]
        total_receita += calc["receita_total"]
        total_direitos += calc["direitos_total"]

    # Ordenação
    if ordenar_por == "receita":
        linhas.sort(key=lambda x: float(x[4][:-1]), reverse=True)  # ordena por receita numérica
    else:
        linhas.sort(key=lambda x: x[0])  # por nome

    # Impressão no estilo de listar_autores
    print("\n" + "=" * 160)
    print(f"{"AUTOR":<50} | {"% DIREITOS":<15} | {"Nº ÁLBUNS":<10} | {"UNID. VENDIDAS":<15} | {"RECEITA (€)":<15} | {"DIREITOS (€)":<15}")
    print("-" * 160)

    ultimo_autor = None
    for l in linhas:
        nome = l[0]
        mostrar_nome = nome if nome != ultimo_autor else ""
        print(f"{mostrar_nome:<50} | {l[1]:<15} | {l[2]:<10} | {l[3]:<15} | {l[4]:<15} | {l[5]:<15}")
        ultimo_autor = nome

    print("-" * 160)
    print(f"{"TOTAL":<50} | {"":<15} | {total_albuns:<10} | {total_unidades:<15} | {total_receita:.2f}€{ '':<6} | {total_direitos:.2f}€{ '':<6}")
    print("=" * 160)

    return linhas  # retorna as linhas para uso posterior se necessário


def gerar_relatorio_autor(nome_autor: str):
    """
    Gera relatório individual para um autor específico.
    """
    if not management.realizar_login():
        print("\nAcesso negado ao relatório. Palavra-passe incorreta.")
        return ""

    autor_encontrado = None
    for autor_data in autores.values():
        if autor_data['artist_name'].lower() == nome_autor.lower():
            autor_encontrado = autor_data
            break

    if not autor_encontrado:
        print(f"Autor '{nome_autor}' não encontrado")
        return ""

    percentagem = f"{autor_encontrado['rights_percentage']:.1f}%"
    calc = calcular_direitos_por_autor(nome_autor)

    # Impressão no estilo de listar_autores (individual)
    print("\n" + "=" * 160)
    print(f"{"AUTOR":<50} | {"% DIREITOS":<15} | {"Nº ÁLBUNS":<10} | {"UNID. VENDIDAS":<15} | {"RECEITA (€)":<15} | {"DIREITOS (€)":<15}")
    print("-" * 160)
    print(f"{nome_autor:<50} | {percentagem:<15} | {calc['num_albuns']:<10} | {calc['unidades_total']:<15} | {calc['receita_total']:.2f}€{ '':<6} | {calc['direitos_total']:.2f}€{ '':<6}")
    print("=" * 160)

    return {
        "Autor": nome_autor,
        "% Direitos": percentagem,
        "Nº Álbuns": calc["num_albuns"],
        "Unid. Vendidas": calc["unidades_total"],
        "Receita (€)": calc["receita_total"],
        "Direitos (€)": calc["direitos_total"]
    }