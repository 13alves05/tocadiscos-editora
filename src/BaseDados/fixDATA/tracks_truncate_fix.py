import shutil
from pathlib import Path

# Caminhos para os ficheiros CSV que queremos corrigir.
# Aqui definimos quais são os ficheiros que o script vai processar.
ALBUMS_TABLE_FIX = Path("data/albums_table.csv")
AUTHORS_TABLE_FIX = Path("data/authors_table.csv")

def add_quotes_around_brackets(file_path: Path):
    """Processa o ficheiro linha a linha e adiciona aspas ao conteúdo que estiver entre [ e ]"""
    
    # Primeiro verificamos se o ficheiro existe mesmo.
    if not file_path.exists():
        print(f"Ficheiro não encontrado: {file_path}")
        return

    # Criamos automaticamente um backup antes de alterar o ficheiro original.
    backup = file_path.with_suffix(file_path.suffix + ".backup")
    shutil.copy(file_path, backup)
    print(f"Backup criado: {backup}")

    lines = []          # Lista onde vamos guardar as linhas já tratadas.
    modified_count = 0  # Contador de quantas linhas foram alteradas.

    # Abrimos o ficheiro original para leitura.
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            original_line = line.rstrip('\n')  # Removemos apenas a quebra de linha.
            new_line = original_line           # Começamos por assumir que a linha não muda.

            # Só mexemos na linha se ela tiver [ e ].
            if '[' in new_line and ']' in new_line:

                # Verificação simples para evitar adicionar aspas a algo que já esteja entre aspas.
                if not (new_line.strip().endswith('"]') and '"' in new_line[:new_line.find('[')]):

                    # Encontramos a posição do primeiro '[' e do último ']'.
                    start = new_line.find('[')
                    end = new_line.rfind(']')

                    # Garantimos que as posições são válidas.
                    if start != -1 and end != -1 and end > start:

                        # Separamos a linha em três partes:
                        before = new_line[:start]        # Tudo antes do '['
                        content = new_line[start:end+1]  # O conteúdo dentro dos []
                        after = new_line[end+1:]         # Tudo depois do ']'

                        # Construímos a nova linha com aspas à volta do conteúdo entre [].
                        new_line = before + '"' + content + '"' + after
                        modified_count += 1  # Contamos esta linha como modificada.

            # Guardamos a linha (alterada ou não) na lista final.
            lines.append(new_line)

    # Reescrevemos o ficheiro original com as linhas já tratadas.
    with open(file_path, 'w', encoding='utf-8-sig') as f:
        f.write('\n'.join(lines) + '\n')

    print(f"Processo concluído!")
    print(f"Linhas modificadas: {modified_count}")
    print(f"Ficheiro actualizado: {file_path}")


# Execução principal do script.
# Aqui chamamos a função para os dois ficheiros definidos no topo.
if __name__ == "__main__":
    print(f"Corrigindo ficheiro: {ALBUMS_TABLE_FIX}")
    add_quotes_around_brackets(ALBUMS_TABLE_FIX)

    print(f"Corrigindo ficheiro: {AUTHORS_TABLE_FIX}")
    add_quotes_around_brackets(AUTHORS_TABLE_FIX)