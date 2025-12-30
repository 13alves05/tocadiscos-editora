import menu
import crud
import history
import management
import reports
import audio

def main():
    while True:
        escolha_menu_principal = menu.menu_principal()

        if escolha_menu_principal == "1":
            while True:
                escolha_menu_autores = menu.menu_autores()

                if escolha_menu_autores == "1":
                    crud.load_autores()

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
                    management.listar_autores()

                elif escolha_menu_pesquisa == "2":
                    print("Pesquisa por álbum ainda não implementada.")
                    input("Pressione ENTER para continuar...\n")

                elif escolha_menu_pesquisa == "3":
                    print("Pesquisa por música ainda não implementada.")
                    input("Pressione ENTER para continuar...\n")

                elif escolha_menu_pesquisa == "0":
                    break  # volta ao menu principal

        elif escolha_menu_principal == "3":
            autorizado = management.realizar_login()
            if not autorizado:
                continue # volta ao menu principal
            while True:
                escolha_menu_relatorio = menu.menu_relatorio()
                if  escolha_menu_relatorio == "1":
                    autor = input("Autor: ")
                    reports.calcular_direitos_por_autor(autor)
                    
                elif escolha_menu_relatorio == "2":
                    reports.gerar_relatorio()
                    
                elif escolha_menu_relatorio == "0":
                    break
        
        elif escolha_menu_principal == "4":
            audio.init_audio() # inicializa o mixer do pygame
            while True:
                escolha_menu_player = menu.menu_player()

                if escolha_menu_player == "1":
                    audio.encontrar_caminho_musica()

                elif escolha_menu_player == "2":
                    audio.reproduzir_musica()

                elif escolha_menu_player == "0":
                    break  # volta ao menu principal
                
        elif escolha_menu_principal == "5":
            while True:
                escolha_menu_historico = menu.menu_historico()
                if  escolha_menu_historico == "1":
                    history.ver_historico()
                    
                elif escolha_menu_historico == "2":
                    history.reverter_snapshot()
                    
                elif escolha_menu_historico == "0":
                    break

        elif escolha_menu_principal == "0":
            print("A sair...")
            break #Fecha o programa

if __name__ == "__main__":
    main()
