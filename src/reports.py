"""
Cálculo os direitos editoriais,
fiz o cálculo da receita como unidades vendidas * preço do álbum por álbum do autor, 
os direitos são a percentagem da receita total, usei o load_autores e load_albuns do crud.py, 
adicionei restrição de senha com auth.py, usei parsing manual para os CSVs porque têm listas com vírgulas, 
adicionei prints para depurar os valores enquanto desenvolvia
"""

from tabulate import tabulate  # importei esta biblioteca para a tabela ficar bem formatada no terminal
from crud import load_autores, load_albuns  # usei as funções do crud.py que os meus colegas fizeram
from auth import is_autorizado  # para verificar a senha antes de mostrar direitos

def calcular_direitos_por_autor(autor):
    # carrego todos os álbuns e filtro só os do autor atual
    todos_albuns = load_albuns()
    albuns_autor = [alb for alb in todos_albuns.values() if alb["artist_name"].lower() == autor["artist_name"].lower()]
    num_albuns = len(albuns_autor)  # conto quantos álbuns o autor tem
    unidades_total = sum(alb["unites_sold"] for alb in albuns_autor)  # somo as unidades vendidas
    receita_total = sum(alb["unites_sold"] * alb["album_price"] for alb in albuns_autor)  # calculo receita total
    direitos_total = receita_total * (autor["rights_percentage"] / 100)  # aplico a percentagem

    print(f"Debug: {autor['artist_name']} - {num_albuns} álbuns, receita {receita_total:.2f}, direitos {direitos_total:.2f}")
      # print para ver se os números batem certo
    return {
        "num_albuns": num_albuns,  # número de álbuns
        "unidades_total": unidades_total,  # unidades vendidas
        "receita_total": receita_total,  # receita total
        "direitos_total": direitos_total  # direitos totais
    }

def gerar_relatorio(ordenar_por="autor"):
    # verifico se o utilizador tem autorização para ver os direitos
    if not is_autorizado():

        return "Acesso negado! Introduza a palavra-passe correta"
    
    autores = load_autores()  # carrego os autores
    linhas = []  # lista para guardar as linhas da tabela
    total_albuns = total_unidades = 0  # totais para somar
    total_receita = total_direitos = 0.0  # totais com decimal
    
    for _, autor in autores.items():
          # loop por cada autor
        calc = calcular_direitos_por_autor(autor)  # calculo para este autor

        linhas.append([
            autor["artist_name"],  # nome do autor
            autor["rights_percentage"],  # percentagem de direitos
            calc["num_albuns"],  # número de álbuns
            calc["unidades_total"],  # unidades vendidas
            calc["receita_total"],  # receita total
            calc["direitos_total"]  # direitos totais
        ])

        total_albuns += calc["num_albuns"]
        total_unidades += calc["unidades_total"]
        total_receita += calc["receita_total"]
        total_direitos += calc["direitos_total"]

    # ordenação, se for por receita ordena decrescente, senão por nome
    if ordenar_por == "receita":

        linhas.sort(key=lambda x: x[4], reverse=True)  # ordena por receita decrescente

    else:

        linhas.sort(key=lambda x: x[0])  # ordena por nome do autor
    
    # adiciono linha total no final
    linhas.append(["Total", "", total_albuns, total_unidades, total_receita, total_direitos])
    
    # formato os números para ficar bonito, % com uma casa decimal e valores com duas
    formatadas = [[l[0], f"{l[1]:.1f}%", l[2], l[3], f"{l[4]:.2f}", f"{l[5]:.2f}"] for l in linhas]
    cabecalhos = ["Autor", "% Direitos", "Nº Álbuns", "Unid. Vendidas", "Receita (€)", "Direitos (€)"]

    return tabulate(formatadas, cabecalhos, tablefmt="grid")  # devolve a tabela

if __name__ == "__main__":
    
    print(gerar_relatorio("receita"))  # teste rápido ordenação por receita