import csv

# Listas globais onde os dados ficam carregados em memória
lista_admins = []      # utilizadores autorizados (login)
lista_albuns = []
lista_autores = []
lista_musicas = []


def carregar_dados_sistema():
    """
    Carrega todos os dados dos ficheiros CSV para a memória.
    Esta função deve ser chamada uma vez no arranque da aplicação.
    """
    global lista_admins, lista_albuns, lista_autores, lista_musicas

    try:
        with open("data/admin_table.csv", mode="r", encoding="utf-8") as f:
            lista_admins = list(csv.DictReader(f))

        with open("data/albums_table.csv", mode="r", encoding="utf-8") as f:
            lista_albuns = list(csv.DictReader(f))

        with open("data/authors_table.csv", mode="r", encoding="utf-8") as f:
            lista_autores = list(csv.DictReader(f))

        with open("data/raw_tracks.csv", mode="r", encoding="utf-8") as f:
            lista_musicas = list(csv.DictReader(f))

        print("Dados carregados para a memória.")

    except FileNotFoundError as e:  # caso algum ficheiro não exista
        print(f"Erro: ficheiro {e.filename} não encontrado.")


def realizar_login():
    """
    A função percorre a lista de administradores carregada em memória
    e verifica se existe uma combinação válida de utilizador e senha.
    """
    print("\n--- ACESSO RESTRITO ---")
    username = input("Utilizador: ")
    password = input("Senha: ")

    for admin in lista_admins:
        if admin["username"] == username and admin["password"] == password:
            print("Acesso autorizado.")
            return True

    print("Acesso negado.")
    return False


def listar_autores(autenticado):
    """
    Lista os autores representados pela editora.
    Os direitos editoriais só são mostrados se o utilizador estiver autenticado.
    """
    if not lista_autores:
        print("\nNenhum autor registado.")
        return

    print("\n" + "=" * 100)
    if autenticado:
        print(f"{'ARTISTA':<25} | {'NACIONALIDADE':<20} | {'ÁLBUNS':<40} | {'DIREITOS'}")
    else:
        print(f"{'ARTISTA':<25} | {'NACIONALIDADE':<20} | {'ÁLBUNS':<40}")
    print("-" * 100)

    for autor in lista_autores:
        # album_title está guardado como string no CSV
        albuns = autor.get("album_title", "N/A")

        if autenticado:
            print(
                f"{autor['artist_name']:<25} | "
                f"{autor['artist_nacionality']:<20} | "
                f"{albuns:<40} | "
                f"{autor.get('rights_percentage', 'N/A')}%"
            )
        else:
            print(
                f"{autor['artist_name']:<25} | "
                f"{autor['artist_nacionality']:<20} | "
                f"{albuns:<40}"
            )

    print("=" * 100)


def listar_albuns():
    """
    Lista os álbuns registados na editora, com todas as informações exigidas
    pelo enunciado.
    """
    if not lista_albuns:
        print("\nNenhum álbum registado.")
        return

    print("\n" + "=" * 120)
    print(
        f"{'ÁLBUM':<25} | {'ARTISTA':<20} | {'GÉNERO':<15} | "
        f"{'LANÇAMENTO':<12} | {'VENDAS':<8} | {'PREÇO':<8} | {'MÚSICAS'}"
    )
    print("-" * 120)

    for alb in lista_albuns:
        musicas = alb.get("tracks", "N/A")

        try:
            preco = float(alb["album_price"])
        except ValueError:
            preco = 0.0

        print(
            f"{alb['album_title']:<25} | "
            f"{alb['artist_name']:<20} | "
            f"{alb['album_genere']:<15} | "
            f"{alb.get('album_date', 'N/A'):<12} | "
            f"{alb['unites_sold']:<8} | "
            f"{preco:<8.2f} | "
            f"{musicas}"
        )

    print("=" * 120)


# RELATÓRIO FINANCEIRO (ACESSO RESTRITO)
# NOTA: Este relatório é uma versão simples para demonstração
# O relatório completo e final encontra-se implementado em reports.py


def gerar_relatorio_financeiro(autenticado):
    if not autenticado:
        print("\nAcesso negado ao relatório financeiro.")
        return

    print("\n" + "RELATÓRIO DE DIREITOS EDITORIAIS".center(80))
    print("-" * 80)
    print(f"{'Autor':<20} | {'% Direitos':<12} | {'Receita (€)':<15} | {'Direitos (€)'}")
    print("-" * 80)

    total_global = 0.0

    for autor in lista_autores:
        try:
            nome = autor["artist_name"]
            percentagem = float(autor["rights_percentage"])
            receita = float(autor.get("total_earned", 0))

            direitos = receita * (percentagem / 100)
            total_global += direitos

            print(
                f"{nome:<20} | "
                f"{percentagem:>10.1f}% | "
                f"{receita:>13.2f}€ | "
                f"{direitos:>12.2f}€"
            )

        except (KeyError, ValueError):
            continue

    print("-" * 80)
    print(f"{'TOTAL GERAL':<49} | {total_global:>12.2f}€")
    print("=" * 80)