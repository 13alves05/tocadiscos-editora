"""
Cálculo dos direitos editoriais,
fiz o cálculo da receita como unidades vendidas * preço do álbum por álbum do autor, 
os direitos são a percentagem da receita total, usei o load_autores e load_albuns do crud.py, 
adicionei restrição de senha com management.py (realizar_login), usei parsing manual para os CSVs porque têm listas com vírgulas, 
adicionei prints para depurar os valores enquanto desenvolvia
"""

from tabulate import tabulate  # importei esta biblioteca para a tabela ficar bem formatada no terminal
from crud import load_autores, load_albuns  # usei as funções do crud.py que os meus colegas fizeram
import management  # para usar a função realizar_login e controlar acesso ao relatório

def calcular_direitos_por_autor(autor):
    # carrego todos os álbuns e filtro só os do autor atual (comparação em minúsculas para evitar problemas de maiúsculas)
    todos_albuns = load_albuns()
    albuns_autor = [alb for alb in todos_albuns.values() if alb["artist_name"].lower() == autor["artist_name"].lower()]
    
    num_albuns = len(albuns_autor)  # conto quantos álbuns o autor tem
    
    # somo as unidades vendidas de todos os álbuns do autor
    unidades_total = sum(int(alb["unites_sold"]) for alb in albuns_autor)
    
    # calculo a receita total: unidades vendidas * preço do álbum para cada álbum
    receita_total = sum(int(alb["unites_sold"]) * float(alb["album_price"]) for alb in albuns_autor)
    
    # aplico a percentagem de direitos contratada
    direitos_total = receita_total * (autor["rights_percentage"] / 100)

    # print de debug para ver se os números estão corretos durante os testes
    # print(f"Debug: {autor['artist_name']} - {num_albuns} álbuns, {unidades_total} unidades vendidas, receita {receita_total:.2f}€, direitos {direitos_total:.2f}€")

    return {
        "num_albuns": num_albuns,
        "unidades_total": unidades_total,
        "receita_total": receita_total,
        "direitos_total": direitos_total
    }

def gerar_relatorio(ordenar_por="autor"):
    # Primeiro verifico se o utilizador está autenticado (conforme o enunciado)
    if not management.realizar_login():
        print("\nAcesso negado ao relatório. Palavra-passe incorreta.")
        return ""

    autores = load_autores()  # carrego os autores da tabela processada
    linhas = []  # lista para guardar as linhas da tabela
    total_albuns = total_unidades = 0
    total_receita = total_direitos = 0.0

    for _, autor in autores.items():
        calc = calcular_direitos_por_autor(autor)  # cálculo específico para este autor

        linhas.append([
            autor["artist_name"],
            autor["rights_percentage"],
            calc["num_albuns"],
            calc["unidades_total"],
            calc["receita_total"],
            calc["direitos_total"]
        ])

        # acumulo os totais gerais
        total_albuns += calc["num_albuns"]
        total_unidades += calc["unidades_total"]
        total_receita += calc["receita_total"]
        total_direitos += calc["direitos_total"]

    # ordenação: por receita (decrescente) ou por nome do autor (alfabética)
    if ordenar_por == "receita":
        linhas.sort(key=lambda x: x[4], reverse=True)
    else:
        linhas.sort(key=lambda x: x[0])

    # linha de total no fim da tabela
    linhas.append(["TOTAL", "", total_albuns, total_unidades, total_receita, total_direitos])

    # formato os valores para ficar bonito: percentagem com 1 casa, dinheiro com 2 casas
    formatadas = [[l[0], f"{l[1]:.1f}%" if isinstance(l[1], (int, float)) else l[1],
                   l[2], l[3], f"{l[4]:.2f}€", f"{l[5]:.2f}€"] for l in linhas]

    cabecalhos = ["Autor", "% Direitos", "Nº Álbuns", "Unid. Vendidas", "Receita (€)", "Direitos (€)"]

    # devolvo a tabela formatada com tabulate (fica muito mais legível no terminal)
    print("\n" + "="*100)
    print("RELATÓRIO DE DIREITOS EDITORIAIS".center(100))
    print("="*100)
    tabela = tabulate(formatadas, cabecalhos, tablefmt="grid")
    print(tabela)
    print("="*100)

    return tabela  # devolvo também como string caso seja usado na GUI