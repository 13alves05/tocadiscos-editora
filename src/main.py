import menu
import crud
import history
import management
import reports
import audio
import ast
from searchEngine import search, build_unified_index

build_unified_index()
management.carregar_dados_sistema()

def main():
    while True:
        escolha_menu_principal = menu.menu_principal()

        if escolha_menu_principal == "1":
            while True:
                escolha_menu_pesquisa = menu.menu_pesquisa()

                if escolha_menu_pesquisa == "1":
                    print("Para a vizualização dos direitos autorais, é necessário efetuar login\n")
                    # Listar autores - se quiser ver os direitos tem de fazer login
                    autenticado = management.realizar_login()  # pede senha se necessário
                    management.listar_autores(autenticado)  # passa True ou False para mostrar/esconder direitos

                elif escolha_menu_pesquisa == "2":
                    termo = input("Pesquisar autor: ")
                    resultados = search(termo, filter_type="artist")
                    if not resultados:
                        print("\nNenhum autor encontrado.")
                        break
                    for r in resultados:
                        print(f"Autor: {r["artist_name"]} - Gênero: {r.get('genres', "N/A")} - Nacionalidade: {r['nationality']}")

                elif escolha_menu_pesquisa == "3":
                    termo = input("Pesquisar álbum: ")
                    resultados = search(termo, filter_type="album")
                    if not resultados:
                        print("\nNenhum álbum encontrado.")
                        break
                    album_tracks = resultados[0]['track_list']
                    track_list = ast.literal_eval(album_tracks)
                    for r in resultados:
                        print(f"Album: {r['title']} by {r['artist_name']} - Gênero: {r.get('genres', "N/A")} - Data de lançamento: {r['album_date']} - Preço: {r.get('album_price', "N/A")} - Vendido: {r.get('unites_sold', 'N/A')} unidades")
                    nomes_musicas = [track[1] for track in track_list]
                    print("Músicas:", ", ".join(nomes_musicas))

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

        elif escolha_menu_principal == "2":
            autorizado = management.realizar_login()
            if not autorizado:
                print("\nAcesso negado ao menu administrador.")
                continue
            while True:
                escolha_menu_administrador = menu.menu_administrador()
                if escolha_menu_administrador == "1":
                    autor = input("Autor: ")
                    reports.gerar_relatorio_autor(autor)
                    
                elif escolha_menu_administrador == "2":
                    management.gerar_relatorio_financeiro(autorizado)
                
                elif escolha_menu_administrador == "3":
                    crud.adicionar_autor()

                elif escolha_menu_administrador == "4":
                    autor = input("Autor que deseja remover: ")
                    crud.remover_autor(autor)
                    
                elif escolha_menu_administrador == "0":
                    break
        
        elif escolha_menu_principal == "3":
            while True:
                escolha_menu_player = menu.menu_player()

                if escolha_menu_player == "1":
                    audio.init_audio()
                    musica = input("Qual música deseja buscar: ")
                    caminho_musica = audio.encontrar_caminho_musica(musica)
                    audio.play_music(caminho_musica)
                
                elif escolha_menu_player == "2":
                    audio.pause_music()
                    print("\nMúsica pausada")

                elif escolha_menu_player == "3":
                    audio.resume_music()
                    print("\nMúsica retomada")

                elif escolha_menu_player == "4":
                    audio.stop_music()
                    print("\nMúsica parada")

                elif escolha_menu_player == "0":
                    break  # volta ao menu principal

                
        elif escolha_menu_principal == "4":
            while True:
                escolha_menu_historico = menu.menu_historico()
                if escolha_menu_historico == "1":
                    print(history.ver_historico())
                    
                elif escolha_menu_historico == "2":
                    nome = input("Nome do snapshot para reverter: ")
                    history.reverter_snapshot(nome)
                    
                elif escolha_menu_historico == "0":
                    break

        elif escolha_menu_principal == "0":
            print("Fechando o programa...")
            break #Fecha o programa

if __name__ == "__main__":
    main()