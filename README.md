# 🎵 Tocadiscos Editora — Sistema de Gestão Musical (CLI)

**Projeto Académico – Gestão de Catálogo Musical**  
**Unidade Curricular:** Algoritmos e Programação  
**Curso:** Desenvolvimento de Software  
**Ano Letivo:** 2025/2026  

A **Tocadiscos Editora** é uma aplicação em linha de comandos (CLI) desenvolvida para gerir o catálogo musical de uma editora fictícia.  
O sistema permite gerir **autores, álbuns e músicas**, calcular **direitos editoriais**, realizar **pesquisas avançadas**, reproduzir áudio e manter um **histórico completo de alterações** com possibilidade de reversão.

Todos os dados são armazenados em ficheiros **CSV**, com validação rigorosa e pré‑processamento automático.

---

# 🧑‍💻 Autoria

Projeto desenvolvido por:

- **Bruno Oliveira**  
- **Gabriela Tavares**  
- **Leonardo Alves**  
- **Vinicius Toniato**

---

# 📜 Objetivo do Projeto

O projeto cumpre integralmente o enunciado da UC **Algoritmos e Programação**, incluindo:

- Menu navegável em CLI  
- Gestão de autores, álbuns e músicas  
- Cálculo de direitos editoriais  
- Relatórios tabulares com totais  
- Pesquisa por autor, álbum ou música  
- Reprodução de áudio  
- Histórico de ações com reversão  
- Armazenamento em `.csv`  
- Acesso restrito a funcionalidades sensíveis  

---

# 🚀 Visão Geral da Aplicação

A aplicação está dividida em **quatro grandes áreas funcionais**:

## 🔍 1. Pesquisa (Whoosh Search Engine)
- Pesquisa rápida por **autor**, **álbum** ou **música**  
- Indexação unificada de todos os CSV  
- Resultados estruturados e filtrados por tipo  
- Reconstrução automática do índice após alterações  

## 🧑‍💼 2. Administração (Acesso Restrito)
- Adicionar novos autores  
- Remover autores (com eliminação em cascata de álbuns e músicas)  
- Gerar relatório financeiro completo  
- Gerar relatório individual por autor  

## 🎧 3. Player de Áudio
- Reproduzir músicas por título  
- Pausar, retomar e parar  
- Caminhos de áudio gerados automaticamente com base no `track_id`  

## 🕒 4. Histórico e Snapshots
- Cada alteração importante gera um snapshot automático  
- Snapshots incluem cópia dos CSV + meta.json  
- Possibilidade de reverter para qualquer estado anterior  
- Função “Desfazer última ação” com confirmação  

---

# 🧩 Arquitetura e Módulos

A aplicação segue uma estrutura modular clara:

```
src/
├── BaseDados/
│   ├── fixDATA/              # Scripts de pré-processamento dos CSV
│   ├── dataSchema.py         # Validação rigorosa com 'schema'
│   └── getAudioPath.py       # Construção de caminhos de áudio
├── audio.py                  # Player de áudio (pygame)
├── crud.py                   # CRUD + snapshots + escrita/atualização dos CSV
├── history.py                # Sistema de snapshots e reversão
├── main.py                   # Ponto de entrada da aplicação
├── management.py             # Autenticação e carregamento de dados
├── menu.py                   # Menus navegáveis (CLI)
├── reports.py                # Relatórios financeiros
└── searchEngine.py           # Indexação e pesquisa (Whoosh)
```

---

# 🛠️ Funcionalidades Técnicas Implementadas

## ✔️ Validação de Dados (schema)
- Funções auxiliares para validar tipos, datas, listas, inteiros positivos, etc.  
- Esquemas completos para autores, álbuns, músicas e administradores  
- Evita dados mal formatados nos CSV  

## ✔️ Pré‑processamento dos CSV
Scripts em `fixDATA/` corrigem:
- listas mal formatadas  
- campos truncados  
- inconsistências no dataset original  

## ✔️ CRUD Completo
- Adicionar autor  
- Remover autor (com cascade delete)  
- Atualizar percentagens de direitos  
- Escrita segura dos CSV  

## ✔️ Relatórios Financeiros
- Totais por autor  
- Totais globais  
- Direitos editoriais calculados automaticamente  
- Tabelas formatadas com `tabulate`  

## ✔️ Pesquisa Avançada (Whoosh)
- Indexação unificada de autores, álbuns e músicas  
- Pesquisa por múltiplos campos  
- Filtros por tipo de documento  
- Resultados rápidos e consistentes  

## ✔️ Player de Áudio
- Baseado em `pygame.mixer`  
- Caminhos automáticos para ficheiros `.mp3`  
- Controlo completo: iniciar, pausar, retomar, parar  

## ✔️ Histórico e Reversão
- Snapshots automáticos em `data/history/`  
- Cada snapshot contém:
  - CSVs completos  
  - meta.json com descrição e timestamp  
- Reversão manual ou automática  

---

# 📂 Estrutura dos Dados

### `authors_table.csv`
- author_id  
- artist_name  
- artist_nacionality  
- album_title (lista)  
- rights_percentage  
- total_earned  

### `albums_table.csv`
- album_id  
- album_title  
- artist_name  
- album_genere  
- album_date  
- unites_sold  
- album_price  
- tracks (lista)  

### `raw_tracks.csv`
- track_id  
- album_id  
- track_title  
- track_genres  
- track_price  
- artist_name  
- artist_nacionality  
- …  

---

# ▶️ Como Executar

## 1. Requisitos
- Python **3.13+**

## 2. Instalar dependências
```bash
pip install -r requirements.txt
```

## 3. Preparar áudio (opcional)
Criar estrutura:
```
data/songs/000/000001.mp3
data/songs/000/000002.mp3
...
```

## 4. Executar
```bash
python src/main.py
```

## 5. Login de Administrador
```
Utilizador: admin
Senha: admin
```

---

# 🧭 Menus da Aplicação

### Menu Principal
```
1 - Pesquisa
2 - Administrador
3 - Player
4 - Histórico
0 - Sair
```

### Submenus
- Pesquisa: autores, álbuns, músicas  
- Administrador: relatórios, adicionar/remover autores  
- Player: iniciar/pausar/retomar/parar  
- Histórico: ver snapshots e desfazer última ação  

---

# 📝 Notas Finais

- O projeto segue boas práticas de modularidade, validação, segurança e documentação.  
- Todas as operações críticas são registadas e reversíveis.  
- A pesquisa é rápida e escalável graças ao Whoosh.  
- A aplicação é totalmente funcional em CLI, cumprindo todos os requisitos académicos.

---

# 🔗 Repositório GitHub

👉 https://github.com/13alves05/tocadiscos-editora
