def menu_principal():
    # Conjunto de opções válidas para validar a escolha do utilizador
    opcoes_validas = {"1", "2", "3", "4", "0"}

    while True:
        # Menu principal — ponto de entrada da aplicação
        print("\n" + "=" * 40)
        print("        EDITORA TOCADISCOS")
        print("=" * 40)
        print("1 - Pesquisa")
        print("2 - Administrador")
        print("3 - Player")
        print("4 - Histórico")
        print("0 - Sair")
        print("-" * 40)

        escolha = input("Opção: ").strip()

        # Se a escolha for válida, devolve-a ao programa principal
        if escolha in opcoes_validas:
            return escolha

        print("Opção inválida. Tente novamente.")


def menu_pesquisa():
    # Opções válidas para o submenu de pesquisa
    opcoes_validas = {"1", "2", "3", "4", "0"}

    while True:
        print("\n" + "-" * 35)
        print("          MENU PESQUISA")
        print("-" * 35)
        print("1 - Listar autores")
        print("2 - Autor")
        print("3 - Álbum")
        print("4 - Música")
        print("0 - Voltar")
        print("-" * 35)

        escolha = input("Opção: ").strip()

        if escolha in opcoes_validas:
            return escolha

        print("Opção inválida. Tente novamente.")


def menu_administrador():
    # Submenu reservado a utilizadores autenticados
    opcoes_validas = {"1", "2", "3", "4", "0"}

    while True:
        print("\n" + "-" * 38)
        print("        MENU ADMINISTRADOR")
        print("-" * 38)
        print("1 - Direitos por autor")
        print("2 - Relatório Geral")
        print("3 - Adicionar novo autor")
        print("4 - Deletar autor")
        print("0 - Voltar")
        print("-" * 38)

        escolha = input("Opção: ").strip()

        if escolha in opcoes_validas:
            return escolha

        print("Opção inválida. Tente novamente.")


def menu_player():
    # Submenu do player de áudio
    opcoes_validas = {"1", "2", "3", "4", "0"}

    while True:
        print("\n" + "-" * 30)
        print("         MENU PLAYER")
        print("-" * 30)
        print("1 - Iniciar música")
        print("2 - Pausar")
        print("3 - Continuar")
        print("4 - Parar")
        print("0 - Voltar")
        print("-" * 30)

        escolha = input("Opção: ").strip()

        if escolha in opcoes_validas:
            return escolha

        print("Opção inválida. Tente novamente.")


def menu_historico():
    # Submenu do sistema de snapshots
    opcoes_validas = {"1", "2", "0"}

    while True:
        print("\n" + "-" * 34)
        print("        MENU HISTÓRICO")
        print("-" * 34)
        print("1 - Ver histórico")
        print("2 - Desfazer última ação")
        print("0 - Voltar")
        print("-" * 34)

        escolha = input("Opção: ").strip()

        if escolha in opcoes_validas:
            return escolha

        print("Opção inválida. Tente novamente.")