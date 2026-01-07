import menu
import crud
import history
import management
import reports
import audio
import ast
from searchEngine import search, build_unified_index

# Ao iniciar o programa, reconstruímos o índice de pesquisa
# para garantir que está sincronizado com os CSV.
build_unified_index()

# Carregamos os dados iniciais do sistema (autores, álbuns, músicas)
management.carregar_dados_sistema()


def main():
    # Loop principal da aplicação — mantém o programa a correr até o utilizador escolher sair.
    while True:
        escolha_menu_principal = menu.menu_principal()

        # ===================== MENU PESQUISA =====================
        if escolha_menu_principal == "1":
            while True:
                escolha_menu_pesquisa = menu.menu_pesquisa()

                # Listar autores (com ou sem direitos, dependendo do login)
                if escolha_menu_pesquisa == "1":
                    print("Para a vizualização dos direitos autorais, é necessário efetuar login\n")
                    autenticado = management.realizar_login()
                    # Se autenticado=True, mostra direitos; caso contrário, esconde
                    management.listar_autores(autenticado)

                # Pesquisa por autor usando o motor de busca Whoosh
                elif escolha_menu_pesquisa == "2":
                    termo = input("Pesquisar autor: ")
                    resultados = search(termo, filter_type="artist")
                    if not resultados:
                        print("\nNenhum autor encontrado.")
                        break
                    for r in resultados:
                        print(f"Autor: {r['artist_name']} - Gênero: {r.get('genres', 'N/A')} - Nacionalidade: {r['nationality']}")

                # Pesquisa por álbum
                elif escolha_menu_pesquisa == "3":
                    termo = input("Pesquisar álbum: ")
                    resultados = search(termo, filter_type="album")
                    if not resultados:
                        print("\nNenhum álbum encontrado.")
                        break

                    # O campo track_list vem como string -> converter para lista real
                    album_tracks = resultados[0]['track_list']
                    track_list = ast.literal_eval(album_tracks)

                    # Mostra informação do álbum
                    for r in resultados:
                        print(
                            f"Album: {r['title']} by {r['artist_name']} - "
                            f"Gênero: {r.get('genres', 'N/A')} - "
                            f"Data de lançamento: {r['album_date']} - "
                            f"Preço: {r.get('album_price', 'N/A')} - "
                            f"Vendido: {r.get('unites_sold', 'N/A')} unidades"
                        )

                    # Lista as músicas do álbum
                    nomes_musicas = [track[1] for track in track_list]
                    print("Músicas:", ", ".join(nomes_musicas))

                # Pesquisa por música
                elif escolha_menu_pesquisa == "4":
                    termo = input("Pesquisar música: ")
                    resultados = search(termo, filter_type="track")
                    if not resultados:
                        print("\nNenhuma música ou autor encontrado.")
                        input("Pressione ENTER para continuar...")
                        break
                    for r in resultados:
                        print(r["track_title"], "-", r["album_title"], "by", r["artist_name"])

                elif escolha_menu_pesquisa == "0":
                    break  # volta ao menu principal

        # ===================== MENU ADMINISTRADOR =====================
        elif escolha_menu_principal == "2":
            autorizado = management.realizar_login()
            if not autorizado:
                print("\nAcesso negado ao menu administrador.")
                continue

            while True:
                escolha_menu_administrador = menu.menu_administrador()

                # Relatório de um autor específico
                if escolha_menu_administrador == "1":
                    autor = input("Autor: ")
                    reports.gerar_relatorio_autor(autor)

                # Relatório financeiro completo (restrito a admin)
                elif escolha_menu_administrador == "2":
                    management.gerar_relatorio_financeiro(autorizado)

                # Adicionar autor
                elif escolha_menu_administrador == "3":
                    crud.adicionar_autor()

                # Remover autor
                elif escolha_menu_administrador == "4":
                    autor = input("Autor que deseja remover: ")
                    crud.remover_autor(autor)

                elif escolha_menu_administrador == "0":
                    break

        # ===================== MENU PLAYER DE ÁUDIO =====================
        elif escolha_menu_principal == "3":
            while True:
                escolha_menu_player = menu.menu_player()

                # Tocar música
                if escolha_menu_player == "1":
                    audio.init_audio()
                    musica = input("Qual música deseja buscar: ")
                    caminho_musica = audio.encontrar_caminho_musica(musica)
                    audio.play_music(caminho_musica)

                # Pausar
                elif escolha_menu_player == "2":
                    audio.pause_music()
                    print("\nMúsica pausada")

                # Retomar
                elif escolha_menu_player == "3":
                    audio.resume_music()
                    print("\nMúsica retomada")

                # Parar
                elif escolha_menu_player == "4":
                    audio.stop_music()
                    print("\nMúsica parada")

                elif escolha_menu_player == "0":
                    break

        # ===================== MENU HISTÓRICO / SNAPSHOTS =====================
        elif escolha_menu_principal == "4":
            while True:
                escolha_menu_historico = menu.menu_historico()

                # Ver histórico de snapshots
                if escolha_menu_historico == "1":
                    print(history.ver_historico())

                # Reverter snapshot
                elif escolha_menu_historico == "2":
                    nome = input("Nome do snapshot para reverter: ")
                    history.reverter_snapshot(nome)

                elif escolha_menu_historico == "0":
                    break

        # ===================== SAIR DO PROGRAMA =====================
        elif escolha_menu_principal == "0":
            print("Fechando o programa...")
            break  # Fecha o programa


if __name__ == "__main__":
    main()