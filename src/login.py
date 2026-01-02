def login():
    """Função de login usando users.csv. Retorna True se sucesso, False caso contrário."""
    print("Para sair, deixe os campos em branco.")
    username = input("Username: ").strip()
    password = input("Senha: ").strip()
    if not username and not password:
        return False
    
    try:
        with open("data/users.csv", 'r') as csv_reader:  # Assumindo pasta 'data/'
            csv_data = csv_reader.readlines()
    except FileNotFoundError:
        print("Ficheiro de utilizadores não encontrado.")
        return False

    for line in csv_data[1:]:  # Salta cabeçalho
        field = line.strip().split(",")
        if len(field) < 3:
            continue
        if field[0].strip() == username and field[1].strip() == password:
            global admin
            admin = field[2].strip() == "admin"
            print("Login bem-sucedido.")
            return True

    print("Username ou senha incorretos. Tente novamente.")
    return login()