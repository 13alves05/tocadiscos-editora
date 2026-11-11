"""
Sistema simples de snapshots para histórico de alterações.

Este módulo permite guardar cópias de segurança dos ficheiros CSV sempre que é feita uma alteração importante
(adicionar autor, remover autor, atualizar direitos, etc.). Cada snapshot fica numa pasta com timestamp
e descrição da ação, acompanhado de um meta.json com metadados.

Funcionalidades:
- salvar_snapshot(acao): cria um novo snapshot
- ver_historico(): lista todos os snapshots disponíveis
- reverter_snapshot(nome): restaura os CSV a partir de um snapshot específico
- desfazer_ultima_acao(): funcionalidade extra que reverte automaticamente a última alteração (com confirmação)

Tudo isto é uma funcionalidade adicional que implementei para tornar a aplicação mais robusta
e permitir recuperar de erros ou alterações indesejadas.
"""

import os
import shutil
import datetime
import json
from pathlib import Path
from searchEngine import build_unified_index

# Pasta onde ficam guardados todos os snapshots.
# Cada snapshot é uma pasta com os CSV copiados e um ficheiro meta.json.
HIST_DIR = "data/history"

# Lista dos ficheiros que queremos incluir em cada snapshot.
FILES = [
    "data/authors_table.csv",
    "data/albums_table.csv",
    "data/raw_tracks.csv"
]


def _cria_pasta():
    """Garante que a pasta 'history' existe. Se não existir, cria-a."""
    os.makedirs(HIST_DIR, exist_ok=True)


def salvar_snapshot(acao: str) -> str:
    """
    Cria um snapshot completo do estado atual dos CSV.

    - Gera uma pasta com timestamp + descrição da ação.
    - Copia os ficheiros CSV para essa pasta.
    - Cria um meta.json com informação sobre a ação e a data.

    Retorna o caminho da pasta criada.
    """
    _cria_pasta()

    # Criamos um timestamp único para identificar o snapshot.
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Nome da pasta inclui timestamp + ação (com espaços substituídos por underscores).
    nome_pasta = f"{ts}_{acao.replace(' ', '_')}"
    pasta = os.path.join(HIST_DIR, nome_pasta)
    os.makedirs(pasta, exist_ok=True)

    # Copiamos cada ficheiro CSV para dentro da pasta do snapshot.
    for ficheiro in FILES:
        if os.path.exists(ficheiro):
            shutil.copy(ficheiro, pasta)

    # Guardamos metadados úteis para consulta posterior.
    meta = {
        "acao": acao,
        "data": ts
    }
    with open(os.path.join(pasta, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"Snapshot salvo: {pasta}")
    return pasta


def ver_historico():
    """
    Lista todos os snapshots existentes na pasta 'history'.

    Para cada snapshot:
    - lê o meta.json (se existir)
    - devolve nome + metadados

    Retorna uma lista de dicionários.
    """
    _cria_pasta()
    snapshots = []

    for entrada in os.listdir(HIST_DIR):
        caminho = os.path.join(HIST_DIR, entrada)

        # Só consideramos pastas (cada snapshot é uma pasta)
        if os.path.isdir(caminho):
            meta_path = os.path.join(caminho, "meta.json")

            # Valores por defeito caso o meta.json esteja ausente ou corrompido
            meta = {"acao": "desconhecida", "data": "desconhecida"}

            if os.path.exists(meta_path):
                try:
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                except:
                    pass  # Se o JSON estiver corrompido, usamos os valores padrão

            snapshots.append({"nome": entrada, "meta": meta})

    print(f"Encontrei {len(snapshots)} snapshot(s) no histórico.")
    return snapshots


def reverter_snapshot(nome: str) -> bool:
    """
    Restaura um snapshot válido, limitado à pasta data/history.

    Rejeita caminhos absolutos, traversal, symlinks externos e snapshots
    incompletos antes de substituir qualquer ficheiro de dados.
    """
    if not nome or nome in (".", "..") or "/" in nome or "\\" in nome:
        print("Nome de snapshot inválido.")
        return False

    history_root = Path(HIST_DIR).resolve()
    caminho_snapshot = (history_root / nome).resolve()

    if caminho_snapshot.parent != history_root or not caminho_snapshot.is_dir():
        print("Snapshot não encontrado ou caminho inválido.")
        return False

    ficheiros_snapshot = [
        (Path(ficheiro), caminho_snapshot / Path(ficheiro).name)
        for ficheiro in FILES
    ]

    # Validar o snapshot completo antes de alterar qualquer dado atual.
    if any(not origem.is_file() for _, origem in ficheiros_snapshot):
        print("Snapshot incompleto. Nenhum ficheiro foi alterado.")
        return False

    for destino, origem in ficheiros_snapshot:
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origem, destino)

    build_unified_index()

    print(f"Estado revertido com sucesso para o snapshot: {nome}")
    return True


def desfazer_ultima_acao() -> bool:
    """
    Reverte automaticamente o snapshot mais recente.

    - Mostra ao utilizador qual foi a última ação
    - Pede confirmação
    - Reverte se o utilizador aceitar
    """
    snapshots = ver_historico()

    if not snapshots:
        print("Não há snapshots para reverter.")
        return False

    # Ordenamos por nome (timestamp no início -> mais recente primeiro)
    snapshots.sort(key=lambda x: x['nome'], reverse=True)
    ultimo = snapshots[0]

    print("\n=== DESFAZER ÚLTIMA AÇÃO ===")
    print(f"Ação: {ultimo['meta'].get('acao', 'desconhecida')}")
    print(f"Data/Hora: {ultimo['meta'].get('data', 'desconhecida')}")
    print(f"Snapshot: {ultimo['nome']}")

    confirma = input("\nQueres mesmo reverter para este estado anterior? (s/n): ").strip().lower()
    if confirma != 's':
        print("Operação cancelada.")
        return False

    sucesso = reverter_snapshot(ultimo['nome'])

    if sucesso:
        # Rebuild do índice após reverter
        try:
            from searchEngine import build_unified_index
            build_unified_index()
            print("Índice de pesquisa atualizado.")
        except Exception as e:
            print(f"Aviso: não consegui rebuildar o índice: {e}")

    return sucesso