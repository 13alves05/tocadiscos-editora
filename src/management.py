import csv
import ast
from tabulate import tabulate

# Estas listas funcionam como "cache" em memória.
# São carregadas no arranque e usadas pelo resto da aplicação.
lista_admins = []      # utilizadores autorizados (login)
lista_albuns = []      # catálogo de álbuns
lista_autores = []     # autores representados
lista_musicas = []     # músicas individuais


def carregar_dados_sistema():
    """
    Carrega todos os dados dos ficheiros CSV para a memória.
    Isto evita estar sempre a abrir ficheiros durante a execução.
    """
    global lista_admins, lista_albuns, lista_autores, lista_musicas

    try:
        # Carrega administradores
        with open("data/admins.csv", mode="r", encoding="utf-8") as f:
            lista_admins = list(csv.DictReader(f))

        # Carrega álbuns
        with open("data/albums_table.csv", mode="r", encoding="utf-8") as f:
            lista_albuns = list(csv.DictReader(f))

        # Carrega autores
        with open("data/authors_table.csv", mode="r", encoding="utf-8") as f:
            lista_autores = list(csv.DictReader(f))

        # Carrega músicas
        with open("data/raw_tracks.csv", mode="r", encoding="utf-8") as f:
            lista_musicas = list(csv.DictReader(f))

        print("Dados carregados para a memória.")

    except FileNotFoundError as e:
        # Caso algum ficheiro esteja em falta, avisamos o utilizador.
        print(f"Erro: ficheiro {e.filename} não encontrado.")


def realizar_login():
    """
    Verifica as credenciais introduzidas pelo utilizador.
    Compara com a lista de administradores carregada em memória.
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
    Lista todos os autores, mostrando ou escondendo os direitos editoriais
    dependendo de o utilizador estar autenticado ou não.
    Também trata casos em que o autor não tem álbuns registados.
    """

    if not lista_autores:
        print("\nNenhum autor registado.")
        return

    print()
    print("=" * 90)
    header = (
        f"{'ARTISTA':<30} | {'NACIONALIDADE':<20} | "
        f"{'ÁLBUM':<35} | {'DIREITOS'}"
    )
    print(header)
    print("-" * 90)

    ultimo_artista = None
    ultima_nacionalidade = None

    for autor in lista_autores:
        nome = autor.get("artist_name", "N/A").strip() or "N/A"
        nacionalidade = autor.get("artist_nacionality", "N/A").strip() or "N/A"

        # === EXTRAÇÃO SEGURA DO ÁLBUM ===
        album_raw = autor.get("album_title", "")

        if not album_raw or album_raw.strip() in ("", "N/A", "[]"):
            album = "Sem álbum registado"
        else:
            try:
                albums_list = ast.literal_eval(album_raw.strip())
                if isinstance(albums_list, list) and len(albums_list) > 0:
                    primeiro = albums_list[0]
                    # Se for tuplo (id, nome), usa o nome
                    if isinstance(primeiro, tuple) and len(primeiro) >= 2:
                        album = str(primeiro[1]).strip()
                    else:
                        album = str(primeiro).strip()
                else:
                    album = "Sem álbum registado"
            except Exception:
                album = "Sem álbum registado"

        # === DIREITOS EDITORIAIS (visíveis só para utilizadores autenticados) ===
        if autenticado:
            perc_raw = autor.get("rights_percentage")
            try:
                if perc_raw is None or str(perc_raw).strip() == "":
                    direitos = "N/A"
                else:
                    perc = float(perc_raw)
                    direitos = f"{perc:.1f}%"
            except (ValueError, TypeError):
                direitos = "N/A"
        else:
            direitos = "[ACESSO RESTRITO]"

        # === EVITA REPETIÇÃO DE ARTISTA/NACIONALIDADE EM LINHAS SEGUIDAS ===
        mostrar_artista = nome if nome != ultimo_artista else ""
        mostrar_nacionalidade = nacionalidade if nacionalidade != ultima_nacionalidade else ""

        formatted_line = (
            f"{mostrar_artista:<30} | {mostrar_nacionalidade:<20} | "
            f"{album:<35} | {direitos}"
        )
        print(formatted_line)

        ultimo_artista = nome
        ultima_nacionalidade = nacionalidade

    print("=" * 90)


def listar_albuns():
    """
    Lista todos os álbuns com as suas informações principais.
    """
    if not lista_albuns:
        print("\nNenhum álbum registado.")
        return

    print("\n--- CATÁLOGO DE ÁLBUNS ---")

    for alb in lista_albuns:
        title = alb.get("album_title", "Sem título")
        genero = alb.get("album_genere", "N/A")
        data_lanc = alb.get("album_date", "N/A")
        unidades_vend = alb.get("unites_sold", "0")
        preco = alb.get("album_price", "0.00")
        tracks = alb.get("tracks", "N/A")

        print("\nÁlbum:", title)
        print("  Género:", genero)
        print("  Data de lançamento:", data_lanc)
        print("  Unidades vendidas:", unidades_vend)
        print("  Preço:", preco, "€")
        print("  Músicas:", tracks)
        print("-" * 60)


def gerar_relatorio_financeiro(autenticado):
    """
    Gera o relatório financeiro completo da editora.
    Só pode ser acedido por utilizadores autenticados.
    Calcula:
    - nº de álbuns por autor
    - unidades vendidas
    - receita total
    - direitos editoriais
    """

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

    # Função auxiliar para truncar nomes longos
    def truncate(text, max_len=40):
        text = str(text)
        return text if len(text) <= max_len else text[:max_len - 3] + "..."

    # Primeiro percorremos os álbuns para somar unidades e contar quantos álbuns cada autor tem
    for album in lista_albuns:
        try:
            autor = album["artist_name"]
            unidades = int(album["unites_sold"])
            unidades_totais += unidades

            albuns_por_autor.setdefault(autor, set()).add(album["album_title"])
            unidades_por_autor[autor] = unidades_por_autor.get(autor, 0) + unidades

        except (KeyError, ValueError, TypeError):
            continue

    # Agora percorremos os autores para calcular direitos e receita
    for autor in lista_autores:
        try:
            nome = autor["artist_name"]

            # Percentagem de direitos
            percent_raw = autor.get("rights_percentage", "0")
            percentagem = float(percent_raw.replace("%", ""))

            # Receita total acumulada (mock data)
            receita = float(autor["total_earned"])

            num_albuns = len(albuns_por_autor.get(nome, set()))
            unidades = unidades_por_autor.get(nome, 0)
            albuns_totais += num_albuns

            # Cálculo dos direitos editoriais
            direitos = receita * (percentagem / 100)

            receita_total += receita
            total_global += direitos

            dados.append({
                "Autor": truncate(nome, 40),
                "% Direitos": percentagem,
                "Nº Albuns": num_albuns,
                "Unid. Vendidas": unidades,
                "Receita (€)": f"{receita:.2f} €",
                "Direitos (€)": f"{direitos:.2f} €"
            })

        except (KeyError, ValueError, AttributeError):
            continue

    # Linha final com totais globais
    dados.append({
        "Autor": "TOTAL",
        "% Direitos": "",
        "Nº Albuns": albuns_totais,
        "Unid. Vendidas": unidades_totais,
        "Receita (€)": f"{receita_total:.2f} €",
        "Direitos (€)": f"{total_global:.2f} €"
    })

    # Impressão em formato tabular bonito
    print(
        tabulate(
            dados,
            headers="keys",
            tablefmt="rst",
            numalign="right",
            colalign="right",
            floatfmt=".2f",
        )
    )