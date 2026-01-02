import csv

lista_admins = []  # utilizadores autorizados (login)
lista_albuns = []
lista_autores = []
lista_musicas = []


def carregar_dados_sistema():  # carrega todos os dados dos ficheiros CSV para a memória
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

    print("\n" + "=" * 100)
    if autenticado:
        print(f"{"ARTISTA":<25} | {"NACIONALIDADE":<20} | {"ÁLBUNS":<40} | {"DIREITOS"}")
    else:
        print(f"{"ARTISTA":<25} | {"NACIONALIDADE":<20} | {"ÁLBUNS":<40}")
    print("-" * 100)

    for autor in lista_autores:
        # Se quiseres usar album_title como lista real, faz: albuns = ast.literal_eval(autor['album_title'])
        # Mas aqui uso como string para simplicidade
        albuns = autor.get('album_title', 'N/A')
        if autenticado:
            print(f"{autor['artist_name']:<25} | {autor['artist_nacionality']:<20} | {albuns:<40} | {autor.get('rights_percentage', 'N/A')}%")
        else:
            print(f"{autor['artist_name']:<25} | {autor['artist_nacionality']:<20} | {albuns:<40}")

    print("=" * 100)


def listar_albuns():  # lista os álbuns de cada autor
    if not lista_albuns:
        print("\nNenhum álbum registrado.")
        return

    print("\n" + "=" * 120)
    print(f"{"ÁLBUM":<25} | {"ARTISTA":<20} | {"GÊNERO":<15} | {"LANÇAMENTO":<12} | {"VENDAS":<8} | {"PREÇO":<8} | {"MÚSICAS"}")
    print("-" * 120)

    for alb in lista_albuns:
        musicas = alb.get('tracks', 'N/A')  # Lista de músicas
        print(f"{alb['album_title']:<25} | {alb['artist_name']:<20} | {alb['album_genere']:<15} | {alb.get('album_date', 'N/A'):<12} | {alb['unites_sold']:<8} | {alb['album_price']:<8.2f} | {musicas}")

    print("=" * 120)


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

            # Converte a percentagem de str para número (assume que é número puro, sem '%')
            percentagem = float(autor["rights_percentage"])

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