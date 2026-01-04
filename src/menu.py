def menu_principal():
    opcoes_validas = {"1", "2", "3", "4", "0"}
    while True:
        print("\n=== EDITORA TOCADISCOS ===")
        print("1 - Pesquisa")
        print("2 - Adminstrador")
        print("3 - Player")
        print("4 - Histórico")
        print("0 - Sair")
        escolha = input("Opção: ").strip()
        if escolha in opcoes_validas:
            return escolha
        print("Opção inválida. Tente novamente.")

def menu_pesquisa():
    opcoes_validas = {"1", "2", "3", "4", "0"}
    while True:
        print("\n--- MENU PESQUISA ---")
        print("1 - Listar autores")
        print("2 - Autor")
        print("3 - Album")
        print("4 - Musica")
        print("0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha in opcoes_validas:
            return escolha
        print("Opção inválida. Tente novamente.")

def menu_administrador():
    opcoes_validas = {"1", "2", "3", "4", "0"}
    while True:
        print("\n--- MENU ADMINISTRADOR ---")
        print("1 - Direitos por autor")
        print("2 - Relatório Geral")
        print("3 - Adicionar novo autor")
        print("4 - Deletar autor")
        print("0 - Voltar")
        escolha = input("Opção: ").strip()
        if escolha in opcoes_validas:
            return escolha
        print("Opção inválida. Tente novamente.")

def menu_player():
    opcoes_validas = {"1", "2","3","4", "0"}
    while True:
        print("\n--- MENU PLAYER ---")
        print("1 - Iniciar música")
        print("2 - Pausar")
        print("3 - Continuar")
        print("4 - Parar")
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