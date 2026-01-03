import menu
import crud
import history
import management
import reports
import audio
from searchEngine import search, build_unified_index

build_unified_index()
management.carregar_dados_sistema()

def main():
    while True:
        escolha_menu_principal = menu.menu_principal()

        if escolha_menu_principal == "1":
            while True:
                escolha_menu_autores = menu.menu_autores()

                if escolha_menu_autores == "1":
                    # Listar autores - se quiser ver os direitos tem de fazer login
                    autenticado = management.realizar_login()  # pede senha se necessário
                    management.listar_autores(autenticado)  # passa True ou False para mostrar/esconder direitos

                elif escolha_menu_autores == "2":
                    crud.adicionar_autor()

                elif escolha_menu_autores == "3":
                    autor = input("Autor que deseja remover: ")
                    crud.remover_autor(autor)

                elif escolha_menu_autores == "0":
                    break  # volta ao menu principal

        elif escolha_menu_principal == "2":
            while True:
                escolha_menu_pesquisa = menu.menu_pesquisa()

                if escolha_menu_pesquisa == "1":
                    termo = input("Pesquisar autor: ")
                    resultados = search(termo, filter_type="artist")
                    for r in resultados:
                        print(r["artist_name"])
                    input("Pressione ENTER para continuar...")     

                elif escolha_menu_pesquisa == "2":
                    termo = input("Pesquisar álbum: ")
                    resultados = search(termo, filter_type="album")
                    for r in resultados:
                        print(r["album_title"], "-", r["artist_name"])
                    input("Pressione ENTER para continuar...\n")

                elif escolha_menu_pesquisa == "3":
                    termo = input("Pesquisar música: ")
                    resultados = search(termo, filter_type="track")
                    for r in resultados:
                        print(r["track_title"], "-", r["album_title"], "by", r["artist_name"])
                    input("Pressione ENTER para continuar...\n")

                elif escolha_menu_pesquisa == "0":
                    break  # volta ao menu principal

        elif escolha_menu_principal == "3":
            autorizado = management.realizar_login()
            if not autorizado:
                print("Acesso negado ao menu de relatórios.")
                input("Pressione ENTER para continuar...")
                continue
            while True:
                escolha_menu_relatorio = menu.menu_relatorio()
                if escolha_menu_relatorio == "1":
                    autor = input("Autor: ")
                    # aqui ficaria a funcionalidade de relatório individual (ainda não feita)
                    print(f"Relatório individual de {autor} - em desenvolvimento")
                    input("Pressione ENTER para continuar...")
                    
                elif escolha_menu_relatorio == "2":
                    reports.gerar_relatorio()
                    
                elif escolha_menu_relatorio == "0":
                    break
        
        elif escolha_menu_principal == "4":
            audio.init_audio() # inicializa o mixer do pygame
            while True:
                escolha_menu_player = menu.menu_player()

                if escolha_menu_player == "1":
                    # Selecionar música (ainda sem implementação completa)
                    print("Funcionalidade de seleção em desenvolvimento")
                    input("Pressione ENTER para continuar...")

                elif escolha_menu_player == "2":
                    titulo = input("Título da música para reproduzir: ")
                    audio.reproduzir_musica(titulo)

                elif escolha_menu_player == "0":
                    break  # volta ao menu principal
                
        elif escolha_menu_principal == "5":
            while True:
                escolha_menu_historico = menu.menu_historico()
                if escolha_menu_historico == "1":
                    history.ver_historico()
                    
                elif escolha_menu_historico == "2":
                    nome = input("Nome do snapshot para reverter: ")
                    history.reverter_snapshot(nome)
                    
                elif escolha_menu_historico == "0":
                    break

        elif escolha_menu_principal == "0":
            print("A sair...")
            break #Fecha o programa

if __name__ == "__main__":
    main()