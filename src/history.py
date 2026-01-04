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
from searchEngine import build_unified_index

# Pasta onde ficam guardados todos os snapshots
HIST_DIR = "data/history"

# Ficheiros que queremos guardar em cada snapshot
FILES = [
    "data/authors_table.csv",
    "data/albums_table.csv",
    "data/raw_tracks.csv"
]


def _cria_pasta():
    """Cria a pasta history se ainda não existir."""
    os.makedirs(HIST_DIR, exist_ok=True)


def salvar_snapshot(acao: str) -> str:
    """
    Guarda um snapshot dos ficheiros CSV atuais.
    
    Parâmetro:
        acao (str): descrição da operação realizada (ex: "Adicionado autor 'Madonna'")
    
    Retorna:
        str: caminho da pasta do snapshot criado
    """
    _cria_pasta()
    
    # Crio um nome único com data/hora + descrição da ação
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_pasta = f"{ts}_{acao.replace(' ', '_')}"
    pasta = os.path.join(HIST_DIR, nome_pasta)
    os.makedirs(pasta, exist_ok=True)

    # Copio cada ficheiro CSV para a pasta do snapshot
    for ficheiro in FILES:
        if os.path.exists(ficheiro):
            shutil.copy(ficheiro, pasta)

    # Guardo metadados num ficheiro JSON (útil para mostrar no histórico)
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
    Lista todos os snapshots existentes.
    
    Retorna uma lista de dicionários com o nome da pasta e os metadados.
    """
    _cria_pasta()
    snapshots = []

    for entrada in os.listdir(HIST_DIR):
        caminho = os.path.join(HIST_DIR, entrada)
        if os.path.isdir(caminho):
            meta_path = os.path.join(caminho, "meta.json")
            meta = {"acao": "desconhecida", "data": "desconhecida"}
            
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                except:
                    pass  # se o JSON estiver corrompido, mantenho o padrão
            
            snapshots.append({"nome": entrada, "meta": meta})

    print(f"Encontrei {len(snapshots)} snapshot(s) no histórico.")
    return snapshots


def reverter_snapshot(nome: str) -> bool:
    """
    Restaura os ficheiros CSV a partir de um snapshot específico.
    
    Parâmetro:
        nome (str): nome da pasta do snapshot (ex: "20260104_123045_Adicionado_autor_Madonna")
    
    Retorna True se sucesso, False se o snapshot não existir.
    """
    caminho_snapshot = os.path.join(HIST_DIR, nome)
    
    if not os.path.isdir(caminho_snapshot):
        print("Snapshot não encontrado.")
        return False

    # Copio os ficheiros do snapshot de volta para a pasta data/
    for ficheiro in FILES:
        origem = os.path.join(caminho_snapshot, os.path.basename(ficheiro))
        if os.path.exists(origem):
            shutil.copy(origem, ficheiro)

    build_unified_index()
    print(f"Estado revertido com sucesso para o snapshot: {nome}")
    return True


def desfazer_ultima_acao() -> bool:
    """
    Funcionalidade extra: reverte automaticamente a última alteração feita.
    
    Mostra a última ação realizada, pede confirmação ao utilizador e reverte se aceitar.
    Muito útil para corrigir erros rapidamente.
    
    Retorna True se revertido com sucesso, False caso contrário.
    """
    snapshots = ver_historico()
    
    if not snapshots:
        print("Não há snapshots para reverter.")
        return False

    # Ordeno pelo nome da pasta (o timestamp está no início → mais recente primeiro)
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
        # É importante rebuildar o índice de pesquisa após reverter
        try:
            from searchEngine import build_unified_index
            build_unified_index()
            print("Índice de pesquisa atualizado.")
        except Exception as e:
            print(f"Aviso: não consegui rebuildar o índice: {e}")
    
    return sucesso