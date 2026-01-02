"""
Sistema simples de snapshots para histórico,
copio os ficheiros CSV para data/history/<timestamp>_<action>/,
guardo um meta.json com metadados,
permite listar e reverter snapshots
"""

import os
import shutil
import datetime
import json

HIST_DIR = "data/history"
FILES = ["data/authors_table.csv", "data/albums_table.csv", "data/raw_tracks.csv"]

def _cria_pasta():
    # crio a pasta se não existir
    os.makedirs(HIST_DIR, exist_ok=True)

def salvar_snapshot(acao):
    # salvo um snapshot dos ficheiros
    _cria_pasta()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta = os.path.join(HIST_DIR, f"{ts}_{acao.replace(' ', '_')}")
    os.makedirs(pasta, exist_ok=True)

    for f in FILES:

        if os.path.exists(f):
            shutil.copy(f, pasta)

    meta = {"acao": acao, "data": ts}

    with open(os.path.join(pasta, "meta.json"), "w") as m:

        json.dump(meta, m)

    print(f"Snapshot salvo em {pasta}")  # print para depurar

    return pasta

def ver_historico():
    # mostro os snapshots disponíveis
    _cria_pasta()
    itens = []

    for pasta in os.listdir(HIST_DIR):

        caminho = os.path.join(HIST_DIR, pasta)

        if os.path.isdir(caminho):

            meta_path = os.path.join(caminho, "meta.json")
            meta = {"acao": "desconhecida"}

            if os.path.exists(meta_path):

                with open(meta_path, "r") as m:

                    meta = json.load(m)
                    
            itens.append({"nome": pasta, "meta": meta})

    print(f"Debug: encontrei {len(itens)} snapshots")  # print para depurar

    return itens

def reverter_snapshot(nome):
    # reverto para um snapshot
    src = os.path.join(HIST_DIR, nome)

    if not os.path.isdir(src):

        return "Snapshot não encontrado"
    
    for f in FILES:

        src_f = os.path.join(src, os.path.basename(f))

        if os.path.exists(src_f):

            shutil.copy(src_f, f)

    print(f"Revertido para {nome}")  # print para depurar

    return True