# 🎵 Tocadiscos Editora

**Projeto Académico – Gestão de Catálogo Musical**  
**Unidade Curricular:** Algoritmos e Programação  
**Curso:** Desenvolvimento de Software  
**Ano Letivo:** 2025/2026  

Aplicação em linha de comandos (CLI) desenvolvida para a editora musical fictícia **Tocadiscos**, com o objetivo de apoiar a gestão de **autores, álbuns e músicas**, cálculo automático de **direitos editoriais**, pesquisa de conteúdos, reprodução de áudio e controlo de histórico de alterações.

Os dados são armazenados em ficheiros **CSV**, com base numa adaptação do dataset **Free Music Archive (FMA)**.

---

## 🧑‍💻 Autoria

Projeto desenvolvido por:  
- **Bruno Oliveira**  
- **Gabriela Tavares**  
- **Leonardo Alves**  
- **Vinicius Toniato**  

---

## 🎯 Objetivos do Projeto

Conforme o enunciado do Trabalho Prático (ver imagem anexa ou ficheiro `Enunciado Trabalho Pratico.pdf`):

- Implementar uma aplicação com menu navegável em linha de comandos.
- Gerir autores, álbuns e músicas de uma editora musical.
- Apresentar listagem de autores com nome, nacionalidade, álbuns e percentagem de direitos editoriais (visível apenas após autenticação).
- Apresentar listagem de álbuns por autor com nome, género musical, data de lançamento, unidades vendidas, preço e lista de músicas.
- Armazenar informação em ficheiros `.csv` (formato adaptável pela equipa).
- Calcular automaticamente os direitos editoriais com base na percentagem contratualizada e nas unidades vendidas, apresentando-os em relatório.

---

## ✅ Requisitos do Enunciado (Cumpridos)

| Requisito | Implementação |
|-----------|---------------|
| Menu navegável em linha de comandos | Menus hierárquicos claros (Principal → Pesquisa / Administrador / Player / Histórico) |
| Listagem de autores (nome, nacionalidade, álbuns, % direitos) | Função `listar_autores()` com coluna de direitos condicionada a autenticação |
| Autenticação para informação sensível | Login obrigatório para visualizar % direitos e relatórios financeiros |
| Listagem de álbuns (nome, género, data, unidades vendidas, preço, lista de músicas) | Pesquisa por álbum mostra todas as informações exigidas |
| Armazenamento em ficheiros `.csv` | Três tabelas principais: `authors_table.csv`, `albums_table.csv`, `raw_tracks.csv` |
| Cálculo e relatório de direitos editoriais | Relatório geral e por autor com totais de receita e direitos calculados |

---

## ⭐ Funcionalidades Adicionais

- 🔍 **Pesquisa avançada** por autor, álbum ou música (motor Whoosh)
- 🎧 **Reprodução de áudio** `.mp3` com controlos completos (pygame)
- ✏️ **CRUD** – adição e remoção de autores com eliminação em cascata
- 🕒 **Sistema de histórico** com snapshots automáticos
- ↩️ **Desfazer última ação** com confirmação
- ✔️ **Validação rigorosa** de dados com biblioteca `schema`
- 📊 **Relatórios formatados** em tabelas alinhadas (`tabulate`)

---

## 🗂️ Estrutura do Projeto

```
tocadiscos-editora/
├── data/
│   ├── history/                 # Snapshots automáticos (criado em runtime)
│   ├── songs/                   # Ficheiros de áudio .mp3 (organizados por ID)
│   ├── admins.csv               # Credenciais de administradores
│   ├── albums_table.csv         # Tabela de álbuns
│   ├── authors_table.csv        # Tabela de autores
│   └── raw_tracks.csv           # Tabela de músicas (dados brutos)
├── src/
│   ├── BaseDados/
│   │   ├── fixDATA/             # Scripts auxiliares de pré-processamento
│   │   │   ├── dataFormat.py
│   │   │   ├── organizeData.py
│   │   │   └── tracks_truncate_fix.py
│   │   ├── dataSchema.py        # Validação de dados (schema)
│   │   └── getAudioPath.py      # Construção de caminhos de áudio
│   ├── audio.py                 # Reprodução de áudio (pygame)
│   ├── crud.py                  # Operações CRUD + snapshots
│   ├── history.py               # Gestão de histórico e reversão
│   ├── main.py                  # Ponto de entrada da aplicação
│   ├── management.py            # Carregamento de dados e autenticação
│   ├── menu.py                  # Menus navegáveis
│   ├── reports.py               # Relatórios financeiros
│   └── searchEngine.py          # Indexação e pesquisa (Whoosh)
├── requirements.txt
├── LICENSE                      # MIT License (2025 Toca Discos Editora)
├── Enunciado Trabalho Pratico.pdf
├── Planeamento-pt-pt.txt
└── README.md                    # Este ficheiro
```

---

## 🧭 Funcionalidades da Aplicação

### Menu Principal
```
=== EDITORA TOCADISCOS ===
1 - Pesquisa
2 - Administrador
3 - Player
4 - Histórico
0 - Sair
```

### Pesquisa
- Listagem completa de autores
- Pesquisa específica por autor, álbum ou música

### Administrador (Acesso Restrito)
- Relatório financeiro geral (todos os autores + totais)
- Relatório individual por autor
- Adicionar novo autor
- Remover autor existente

### Player
- Iniciar música (por título)
- Pausar / Continuar / Parar

### Histórico
- Ver lista de snapshots
- Desfazer última ação (com confirmação)

---

## ▶️ Instruções de Execução

### 1. Requisitos
- Python **3.13** ou superior

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```
(ou individualmente: `pygame tabulate schema whoosh pandas`)

### 3. Preparação de áudio (opcional – para testar o Player)
- Criar a pasta `data/songs/`
- Colocar ficheiros `.mp3` organizados por ID da faixa  
  (exemplo: track_id 2 → `data/songs/000/000002.mp3`)
- **Dica de teste rápido:** No menu Player → 1, escreva **Food** (música de exemplo presente no dataset)

### 4. Executar a aplicação
```bash
python src/main.py
```

### 🔐 Credenciais de Administrador
- Utilizador: `admin`
- Senha: `admin`  
(Outros utilizadores definidos em `data/admins.csv`)

---

## 📝 Notas Finais

- Todas as alterações importantes aos dados CSV geram snapshots automáticos em `data/history/`.
- O índice de pesquisa Whoosh é reconstruído automaticamente após alterações.
- O projeto segue boas práticas de modularidade, validação de dados, separação de responsabilidades e documentação extensa no código.

**Repositório GitHub:** https://github.com/13alves05/tocadiscos-editora

**Obrigado pela avaliação!**