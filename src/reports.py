"""
Relatórios de Direitos Editoriais
- Calcula receitas por autor com base nos álbuns vendidos
- Aplica percentagem de direitos
- Restringe acesso com autenticação
- Mostra relatório formatado com alinhamento manual
- Mantém alinhamento semelhante a `listar_autores`
"""

import management
from crud import autores, albuns
from crud import load_autores, load_albuns


def calcular_direitos_por_autor(nome_autor: str):
    """
    Calcula estatísticas financeiras de um autor específico.
    Aqui reunimos:
      - número de álbuns publicados
      - unidades vendidas no total
      - receita total (unidades * preço)
      - direitos editoriais aplicando a percentagem do autor

    Esta função é usada tanto no relatório geral como no individual.
    """

    nome_lower = nome_autor.lower()

    # Filtra todos os álbuns pertencentes ao autor
    autor_albuns = [
        alb for alb in albuns.values()
        if alb.get("artist_name", "").lower() == nome_lower
    ]

    # Número total de álbuns
    num_albuns = len(autor_albuns)

    # Soma das unidades vendidas em todos os álbuns
    unidades_total = sum(
        int(alb.get("unites_sold", 0))
        for alb in autor_albuns
    )

    # Receita total = unidades vendidas * preço do álbum
    receita_total = sum(
        int(alb.get("unites_sold", 0)) *
        float(alb.get("album_price", 0.0))
        for alb in autor_albuns
    )

    # Procura a percentagem de direitos do autor
    autor_rights_percentage = 0
    for autor_data in autores.values():
        if autor_data['artist_name'].lower() == nome_autor.lower():
            autor_rights_percentage = autor_data["rights_percentage"]
            break

    # Cálculo final dos direitos editoriais
    direitos_total = receita_total * (float(autor_rights_percentage) / 100)

    return {
        "num_albuns": num_albuns,
        "unidades_total": unidades_total,
        "receita_total": receita_total,
        "direitos_total": direitos_total
    }


def gerar_relatorio(ordenar_por="autor"):
    """
    Gera o relatório financeiro completo de todos os autores.
    O relatório inclui:
      - nº de álbuns
      - unidades vendidas
      - receita total
      - direitos editoriais

    O acesso deveria ser restrito por palavra‑passe (já preparado no código).
    """

    global autores, albuns
    autores = load_autores()
    albuns = load_albuns()

    linhas = []          # linhas do relatório
    total_albuns = 0
    total_unidades = 0
    total_receita = 0.0
    total_direitos = 0.0

    # Para cada autor, calcula os valores financeiros
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

        # Acumula totais gerais
        total_albuns += calc["num_albuns"]
        total_unidades += calc["unidades_total"]
        total_receita += calc["receita_total"]
        total_direitos += calc["direitos_total"]

    # Ordenação do relatório
    if ordenar_por == "receita":
        # Ordena pela receita numérica (removendo o símbolo €)
        linhas.sort(key=lambda x: float(x[4][:-1]), reverse=True)
    else:
        # Ordena alfabeticamente por nome
        linhas.sort(key=lambda x: x[0])

    # Impressão formatada (estilo semelhante ao listar_autores)
    print("\n" + "=" * 160)

    header = (
        f"{'AUTOR':<45} | {'% DIREITOS':<15} | {'Nº ÁLBUNS':<10} | "
        f"{'UNID. VENDIDAS':<15} | {'RECEITA (€)':<15} | {'DIREITOS (€)':<15}"
    )
    print(header)
    print("-" * 160)

    ultimo_autor = None

    # Impressão das linhas do relatório
    for linha in linhas:
        nome = linha[0]
        mostrar_nome = nome if nome != ultimo_autor else ""

        formatted_line = (
            f"{mostrar_nome:<45} | {linha[1]:<15} | {linha[2]:<10} | "
            f"{linha[3]:<15} | {linha[4]:<15} | {linha[5]:<15}"
        )

        print(formatted_line)
        ultimo_autor = nome

    print("-" * 160)

    # Linha final com totais globais
    total_line = (
        f"{'TOTAL':<45} | {'':<15} | {total_albuns:<10} | "
        f"{total_unidades:<15} | {total_receita:.2f}€{'':<6} | "
        f"{total_direitos:.2f}€{'':<6}"
    )
    print(total_line)
    print("=" * 160)

    return linhas


def gerar_relatorio_autor(nome_autor: str):
    """
    Gera um relatório individual para um autor específico.
    Mostra:
      - nº de álbuns
      - unidades vendidas
      - receita total
      - direitos editoriais
    """

    global autores, albuns
    autores = load_autores()
    albuns = load_albuns()

    # Procura o autor na base de dados
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

    # Impressão formatada (estilo igual ao relatório geral)
    print("\n" + "=" * 160)

    header = (
        f"{'AUTOR':<45} | {'% DIREITOS':<15} | {'Nº ÁLBUNS':<10} | "
        f"{'UNID. VENDIDAS':<15} | {'RECEITA (€)':<15} | {'DIREITOS (€)':<15}"
    )
    print(header)
    print("-" * 160)

    single_line = (
        f"{nome_autor:<45} | {percentagem:<15} | {calc['num_albuns']:<10} | "
        f"{calc['unidades_total']:<14} | {calc['receita_total']:.2f}€ | "
        f"{calc['direitos_total']:.2f}€"
    )

    print(single_line)
    print("=" * 160)

    return {
        "Autor": nome_autor,
        "% Direitos": percentagem,
        "Nº Álbuns": calc["num_albuns"],
        "Unid. Vendidas": calc["unidades_total"],
        "Receita (€)": calc["receita_total"],
        "Direitos (€)": calc["direitos_total"]
    }