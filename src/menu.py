def menu_principal():
    opcoes_validas = {"1", "2", "3", "4", "5", "0"}
    while True:
        print("\n=== EDITORA TOCADISCOS ===")
        print("1 - Autores")
        print("2 - Pesquisa")
        print("3 - Relatórios")
        print("4 - Player")
        print("5 - Histórico")
        print("0 - Sair")
        escolha = input("Opção: ").strip()
        if escolha in opcoes_validas:
            return escolha
        print("Opção inválida. Tente novamente.")

def menu_autores():
    opcoes_validas = {"1", "2", "3", "0"}
    while True:
        print("\n--- MENU AUTORES ---")
        print("1 - Listar autores")
        print("2 - Adicionar novo autor")
        print("3 - Deletar autor")
        print("0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha in opcoes_validas:
            return escolha
        print("Opção inválida. Tente novamente.")

def menu_pesquisa():
    opcoes_validas = {"1", "2", "3", "0"}
    while True:
        print("\n--- MENU PESQUISA ---")
        print("1 - Autor")
        print("2 - Album")
        print("3 - Musica")
        print("0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha in opcoes_validas:
            return escolha
        print("Opção inválida. Tente novamente.")

def menu_relatorio():
    opcoes_validas = {"1", "2", "0"}
    while True:
        print("\n--- MENU RELATÓRIO ---")
        print("1 - Direitos por autor")
        print("2 - Relatório Geral")
        print("0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha in opcoes_validas:
            return escolha
        print("Opção inválida. Tente novamente.")

def menu_player():
    opcoes_validas = {"1", "2", "0"}
    while True:
        print("\n--- MENU PLAYER ---")
        print("1 - Selecionar música")
        print("2 - Reproduzir música")
        print("0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha in opcoes_validas:
            return escolha
        print("Opção inválida. Tente novamente.")

def menu_historico():
    opcoes_validas = {"1", "2", "0"}
    while True:
        print("\n--- MENU HISTÓRICO ---")
        print("1 - Ver histórico")
        print("2 - Desfazer última ação")
        print("0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha in opcoes_validas:
            return escolha
        print("Opção inválida. Tente novamente.")

# if __name__ == "__main__":
#     menu_principal()


# from tabulate import tabulate


# def mostrar_menu(titulo, opcoes):
#     """
#     Mostra um menu genérico formatado com tabulate
#     e retorna a opção escolhida.
#     """
#     print(f"\n=== {titulo} ===\n")

#     tabela = [[k, v] for k, v in opcoes.items()]
#     print(tabulate(tabela, headers=["Opção", "Descrição"], tablefmt="fancy_grid"))

#     while True:
#         escolha = input("Opção: ").strip()
#         if escolha in opcoes:
#             return escolha
#         print("Opção inválida. Tente novamente.")


# # ===== MENUS ESPECÍFICOS =====

# def menu_principal():
#     opcoes = {
#         "1": "Autores",
#         "2": "Pesquisa",
#         "3": "Relatórios",
#         "4": "Player",
#         "5": "Histórico",
#         "0": "Sair"
#     }
#     return mostrar_menu("EDITORA TOCADISCOS", opcoes)


# def menu_autores():
#     opcoes = {
#         "1": "Listar autores",
#         "2": "Adicionar novo autor",
#         "3": "Remover autor",
#         "0": "Voltar"
#     }
#     return mostrar_menu("MENU AUTORES", opcoes)


# def menu_pesquisa():
#     opcoes = {
#         "1": "Pesquisar autor",
#         "2": "Pesquisar álbum",
#         "3": "Pesquisar música",
#         "0": "Voltar"
#     }
#     return mostrar_menu("MENU PESQUISA", opcoes)


# def menu_relatorio():
#     opcoes = {
#         "1": "Calcular direitos por autor",
#         "2": "Gerar relatório geral",
#         "0": "Voltar"
#     }
#     return mostrar_menu("MENU RELATÓRIOS", opcoes)


# def menu_player():
#     opcoes = {
#         "1": "Selecionar música",
#         "2": "Reproduzir música",
#         "0": "Voltar"
#     }
#     return mostrar_menu("PLAYER", opcoes)


# def menu_historico():
#     opcoes = {
#         "1": "Ver histórico",
#         "2": "Desfazer última ação",
#         "0": "Voltar"
#     }
#     return mostrar_menu("MENU HISTÓRICO", opcoes)


# menu_player()