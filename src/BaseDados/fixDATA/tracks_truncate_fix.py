import shutil
from pathlib import Path

# Configura aqui o ficheiro que queres corrigir
ALBUMS_TABLE_FIX = Path("data/albums_table.csv")  # ← muda para o que precisares
AUTHORS_TABLE_FIX = Path("data/authors_table.csv")  # ← muda para o que precisares

def add_quotes_around_brackets(file_path: Path):
    """Processa linha a linha e adiciona aspas à volta de conteúdo entre [ e ]"""
    if not file_path.exists():
        print(f"Ficheiro não encontrado: {file_path}")
        return

    # Backup automático
    backup = file_path.with_suffix(file_path.suffix + ".backup")
    shutil.copy(file_path, backup)
    print(f"Backup criado: {backup}")

    lines = []
    modified_count = 0

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            original_line = line.rstrip('\n')
            new_line = original_line

            # Só processamos se houver [ e ] na linha e ainda não estiver entre aspas
            if '[' in new_line and ']' in new_line:
                # Verifica se já está entre aspas (simples verificação)
                if not (new_line.strip().endswith('"]') and '"' in new_line[:new_line.find('[')]):
                    # Encontra a posição do primeiro [ e último ]
                    start = new_line.find('[')
                    end = new_line.rfind(']')

                    if start != -1 and end != -1 and end > start:
                        # Parte antes do [, o conteúdo entre [] e depois
                        before = new_line[:start]
                        content = new_line[start:end+1]
                        after = new_line[end+1:]

                        # Adiciona aspas apenas ao conteúdo entre [ e ]
                        new_line = before + '"' + content + '"' + after
                        modified_count += 1

            lines.append(new_line)

    # Reescreve o ficheiro original
    with open(file_path, 'w', encoding='utf-8-sig') as f:
        f.write('\n'.join(lines) + '\n')

    print(f"Processo concluído!")
    print(f"Linhas modificadas: {modified_count}")
    print(f"Ficheiro actualizado: {file_path}")


if __name__ == "__main__":
    print(f"Corrigindo ficheiro: {ALBUMS_TABLE_FIX}")
    add_quotes_around_brackets(ALBUMS_TABLE_FIX)
    print(f"Corrigindo ficheiro: {AUTHORS_TABLE_FIX}")
    add_quotes_around_brackets(AUTHORS_TABLE_FIX)
