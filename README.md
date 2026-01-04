# 🎵 Tocadiscos Editora

**Projeto Académico – Gestão de Catálogo Musical**  
**Unidade Curricular:** Algoritmos e Programação  
**Curso:** Desenvolvimento de Software  
**Ano Letivo:** 2025/2026  

Aplicação em linha de comandos (CLI) desenvolvida para a editora musical fictícia **Tocadiscos**, com o objetivo de apoiar a gestão quotidiana de **autores, álbuns e músicas**, cálculo automático de **direitos editoriais**, pesquisa avançada, reprodução de áudio e controlo rigoroso de histórico de alterações.

Os dados são armazenados em ficheiros **CSV**, com base numa adaptação do dataset **Free Music Archive (FMA)**.

---

## 🧑‍💻 Autoria

Projeto desenvolvido por:  
- **Bruno Oliveira**  
- **Gabriela Tavares**  
- **Leonardo Alves**  
- **Vinicius Toniato**  

---

## 📜 Enunciado do Trabalho Prático

O projeto segue fielmente o enunciado fornecido pela unidade curricular **Algoritmos e Programação** (2025/2026), cujos requisitos principais são:

- Menu navegável em linha de comandos  
- Listagem de autores com: Nome, Nacionalidade, Álbuns e Percentagem de direitos editoriais (**visível apenas após autenticação**)  
- Listagem de álbuns por autor com: Nome, Género Musical, Data de Lançamento, Unidades Vendidas, Preço e Lista de músicas  
- Armazenamento em ficheiros `.csv` (formato adaptável)  
- Cálculo automático de direitos editoriais e apresentação em relatório tabular com ordenação, totais por autor e totais gerais (**acesso restrito**)  
- Criação manual de novos autores (atualização dos ficheiros)  
- Remoção de autores e respetivos álbuns  
- Histórico de ações com possibilidade de reversão  
- Pesquisa por autor, álbum ou música  
- Reprodução de ficheiros áudio digitais (sugestão: módulo `pygame.mixer`)

---

## ✅ Requisitos Cumpridos

| Requisito do Enunciado                          | Implementação                                                                 |
|-------------------------------------------------|-------------------------------------------------------------------------------|
| Menu navegável em linha de comandos             | Menus hierárquicos claros (Principal → Pesquisa / Administrador / Player / Histórico) |
| Listagem de autores com % direitos restrita     | `management.listar_autores(autenticado)` – coluna de direitos só visível após login |
| Listagem detalhada de álbuns                    | Pesquisa por álbum mostra todas as informações exigidas                       |
| Armazenamento em `.csv`                         | Três tabelas principais: `authors_table.csv`, `albums_table.csv`, `raw_tracks.csv` |
| Relatório tabular com totais e acesso restrito  | Relatórios geral e por autor com `tabulate`, acesso condicionado a autenticação |
| Criação manual de autores                       | Função `crud.adicionar_autor()`                                               |
| Remoção de autor e álbuns                       | Função `crud.remover_autor()` com eliminação em cascata                       |
| Histórico de ações com reversão                 | Módulo `history.py` – snapshots automáticos + desfazer última ação            |
| Pesquisa por autor/álbum/música                 | Motor Whoosh (`searchEngine.py`) com pesquisa unificada                       |
| Reprodução de áudio                             | Módulo `audio.py` usando `pygame.mixer`                                       |

---

## ⭐ Funcionalidades Adicionais

- 🔍 **Pesquisa avançada e rápida** em todo o catálogo (Whoosh)  
- 🎧 **Player completo** (iniciar, pausar, continuar, parar)  
- 🕒 **Snapshots automáticos** em `data/history/` para todas as alterações importantes  
- ↩️ **Desfazer última ação** com confirmação do utilizador  
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

### Destaques
- **Pesquisa**: Listagem de autores + pesquisa por autor, álbum ou música  
- **Administrador** (acesso restrito): Relatórios financeiros, adicionar/remover autores  
- **Player**: Reprodução de músicas por título  
- **Histórico**: Ver snapshots e desfazer última ação  

---

## ▶️ Instruções de Execução

### 1. Requisitos
- Python **3.13** ou superior

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```
(dependências: `pygame`, `tabulate`, `schema`, `whoosh`, `pandas`)

### 3. Preparação de áudio (opcional – para testar o Player)
- Criar a pasta `data/songs/`
- Colocar ficheiros `.mp3` organizados por ID da faixa  
  (exemplo: track_id 2 → `data/songs/000/000002.mp3`)
- **Dica de teste rápido:** No menu Player → 1, escreva **Food** (música de exemplo do dataset)

### 4. Executar a aplicação
```bash
python src/main.py
```

### 🔐 Credenciais de Administrador
- Utilizador: `admin`
- Senha: `admin`  
(Outros utilizadores podem ser adicionados em `data/admins.csv`)

---

## 📝 Notas Finais

- Todas as alterações importantes geram snapshots automáticos em `data/history/`.
- O índice de pesquisa Whoosh é reconstruído automaticamente após modificações.
- O projeto segue boas práticas de modularidade, validação de dados, segurança de acesso e documentação extensa.

**Repositório GitHub:** https://github.com/13alves05/tocadiscos-editora

**Obrigado**

