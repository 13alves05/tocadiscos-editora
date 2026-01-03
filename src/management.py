import csv

lista_admins = []  # utilizadores autorizados (login)
lista_albuns = []
lista_autores = []
lista_musicas = []


def carregar_dados_sistema():  # carrega todos os dados dos ficheiros CSV para a memória
    global lista_admins, lista_albuns, lista_autores, lista_musicas

    try:
        with open("data/admins.csv", mode="r", encoding="utf-8") as f:
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


def realizar_login():  # A função percorre a lista de administradores carregada em memória e verifica se existe uma combinação válida
    print("\n--- ACESSO RESTRITO ---")
    username = input("Utilizador: ")
    password = input("Senha: ")

    for admin in lista_admins:
        if admin["username"] == username and admin["password"] == password:
            print("Acesso autorizado.")
            return True

    print("Acesso negado.")
    return False


def listar_autores(autenticado):  # lista os autores representados pela editora
    if not lista_autores:
        print("\nNenhum autor registrado.")
        return

    print("\n" + "=" * 80)
    print(f"{"ARTISTA":<25} | {"NACIONALIDADE":<20} | {"DIREITOS"}")
    print("-" * 80)

    for autor in lista_autores:
        nome = autor.get("artist_name", "N/A")
        nacionalidade = autor.get("artist_nacionality", "N/A")

        if autenticado:  # Se o utilizador estiver autenticado, mostra os direitos
            direitos = autor.get("rights_percentage", "N/A")
        else:  # Caso contrário, escondemos a informação sensível
            direitos = "[ACESSO RESTRITO]"

        print(f"{nome:<25} | {nacionalidade:<20} | {direitos}")

    print("=" * 80)


def listar_albuns():  # apresenta a lista de álbuns e respetivas informações
    if not lista_albuns:
        print("\nNenhum álbum registrado.")
        return

    print("\n--- CATÁLOGO DE ÁLBUNS ---")

    for alb in lista_albuns:
        print(f"\nÁlbum: {alb.get( "album_title ",  "Sem título ")}")
        print(f"  Género: {alb.get( "album_genere",  "N/A")}")
        print(f"  Data de lançamento: {alb.get( "album_date ",  "N/A ")}")
        print(f"  Unidades vendidas: {alb.get("unites_sold", "0")}")
        print(f"  Preço: {alb.get( "album_price",  "0.00 ")}€")
        print(f"  Músicas: {alb.get( "tracks ",  "N/A")}")
        print("-" * 60)


# RELATÓRIO FINANCEIRO (ACESSO RESTRITO)


def gerar_relatorio_financeiro(autenticado):
    if not autenticado:
        print("\n Acesso negado ao relatório financeiro.")
        return

    print("\n" + "RELATÓRIO DE DIREITOS EDITORIAIS".center(80))
    print("-" * 80)
    print(
        f"{"Autor":<20} | {"% Direitos":<12} | {"Receita (€)":<15} | {"Direitos (€)"}"
    )
    print("-" * 80)

    total_global = 0.0

    for autor in lista_autores:
        try:
            nome = autor["artist_name"]

            # Converte a percentagem de str para número
            percentagem = float(autor["rights_percentage"].replace("%", ""))

            # Receita usada como mock data para testes
            receita = float(autor["total_earned"])

            # Cálculo dos direitos editoriais
            direitos = receita * (percentagem / 100)
            total_global += direitos

            print(
                f"{nome:<20} | {percentagem:>10.1f}% | {receita:>13.2f}€ | {direitos:>12.2f}€"
            )

        except (KeyError, ValueError):  # Ignora entradas inválidas
            continue

    print("-" * 80)
    print(f"{'TOTAL GERAL':<49} | {total_global:>12.2f}€")
    print("=" * 80)


# BLOCO PRINCIPAL (TESTES / MOCK)

if __name__ == "__main__":
    carregar_dados_sistema()

    utilizador_logado = False

    # Tentativa de acesso ao relatório sem login
    gerar_relatorio_financeiro(utilizador_logado)

    # Processo de login
    utilizador_logado = realizar_login()

    # Funcionalidades após autenticação
    listar_autores(utilizador_logado)
    listar_albuns()
    gerar_relatorio_financeiro(utilizador_logado)