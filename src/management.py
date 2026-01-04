import csv
import ast
from tabulate import tabulate

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

def listar_autores(autenticado):
    if not lista_autores:
        print("\nNenhum autor registado.")
        return

    print("\n" + "=" * 90)
    print(f"{"ARTISTA":<30} | {"NACIONALIDADE":<20} | {"ÁLBUM":<35} | {"DIREITOS"}")
    print("-" * 90)

    ultimo_artista = None
    ultima_nacionalidade = None

    for autor in lista_autores:
        nome = autor.get("artist_name", "N/A").strip() or "N/A"
        nacionalidade = autor.get("artist_nacionality", "N/A").strip()
        if not nacionalidade:
            nacionalidade = "N/A"

        # === EXTRAÇÃO SEGURA DO ÁLBUM ===
        album_raw = autor.get("album_title", "")

        if not album_raw or album_raw.strip() in ("", "N/A", "[]"):
            album = "Sem álbum registado"
        else:
            try:
                albums_list = ast.literal_eval(album_raw.strip())
                if isinstance(albums_list, list) and len(albums_list) > 0:
                    primeiro = albums_list[0]
                    if isinstance(primeiro, tuple) and len(primeiro) >= 2:
                        album = str(primeiro[1]).strip()
                    else:
                        album = str(primeiro).strip()
                else:
                    album = "Sem álbum registado"
            except (ValueError, SyntaxError, Exception):
                album = "Sem álbum registado"

        # === DIREITOS - PROTEGIDO CONTRA None OU VALORES INVÁLIDOS ===
        if autenticado:
            perc_raw = autor.get("rights_percentage")
            try:
                # Se for string vazia, None ou inválido → N/A
                if perc_raw is None or str(perc_raw).strip() == "":
                    direitos = "N/A"
                else:
                    perc = float(perc_raw)
                    direitos = f"{perc:.1f}%"
            except (ValueError, TypeError):
                direitos = "N/A"
        else:
            direitos = "[ACESSO RESTRITO]"

        # === NÃO REPETE ARTISTA/NACIONALIDADE ===
        mostrar_artista = nome if nome != ultimo_artista else ""
        mostrar_nacionalidade = nacionalidade if nacionalidade != ultima_nacionalidade else ""

        print(f"{mostrar_artista:<30} | {mostrar_nacionalidade:<20} | {album:<35} | {direitos}")

        ultimo_artista = nome
        ultima_nacionalidade = nacionalidade

    print("=" * 90)


def listar_albuns():  # apresenta a lista de álbuns e respetivas informações
    if not lista_albuns:
        print("\nNenhum álbum registado.")
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

    total_global = 0.0
    receita_total = 0.0
    unidades_totais = 0
    albuns_totais = 0

    unidades_por_autor = {}
    albuns_por_autor = {}
    dados = []

    for album in lista_albuns:
        try:
            autor = album["artist_name"]
            unidades = int(album["unites_sold"])
            unidades_totais += unidades
            albuns_por_autor.setdefault(autor, set()).add(album["album_title"])
            unidades_por_autor[autor] = unidades_por_autor.get(autor, 0) + unidades

        except (KeyError, ValueError, TypeError):
            continue

    for autor in lista_autores:
        try:
            nome = autor["artist_name"]

            # Converte a percentagem de str para número
            percentagem = float(autor["rights_percentage"].replace("%", ""))

            # Receita usada como mock data para testes
            receita = float(autor["total_earned"])

            
            num_albuns = len(albuns_por_autor.get(nome, set()))
            unidades = unidades_por_autor.get(nome, 0)
            albuns_totais += num_albuns

            # Cálculo dos direitos editoriais
            direitos = receita * (percentagem / 100)
            receita_total += receita
            total_global += direitos
            def truncate(text, max_len=40):
                text = str(text)
                return text if len(text) <= max_len else text[:max_len-3] + "..."
            dados.append({"Autor":truncate(nome, 40),
                     "% Direitos":percentagem,
                     "Nº Albuns":num_albuns,
                     "Unid. Vendidas":unidades,
                     "Receita (€)":f"{receita:.2f} €",
                     "Direitos (€)":f"{direitos:.2f} €",})

        except (KeyError, ValueError, AttributeError):  # Ignora entradas inválidas
            continue
    dados.append({
        "Autor":"TOTAL",
        "% Direitos":"",
        "Nº Albuns":albuns_totais,
        "Unid. Vendidas":unidades_totais,
        "Receita (€)":f"{receita_total:.2f} €",
        "Direitos (€)":f"{total_global:.2f} €"})
    print(tabulate(dados, headers="keys", tablefmt="rst", numalign="right", colalign="right", floatfmt=".2f"))