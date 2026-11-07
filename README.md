# Tocadiscos Editora

Projeto académico de grupo desenvolvido no âmbito da unidade curricular de Algoritmos e Programação, no curso de Desenvolvimento de Software, durante o ano letivo de 2025/2026.

A aplicação é executada na linha de comandos (CLI) e permite gerir o catálogo de uma editora musical fictícia. O sistema trabalha com autores, álbuns e músicas, calcula direitos editoriais, disponibiliza pesquisa, permite reproduzir ficheiros de áudio e mantém um histórico de alterações com possibilidade de reversão.

## Autoria

- Bruno Oliveira
- Gabriela Tavares
- Leonardo Alves
- Vinicius Toniato

## Funcionalidades

- Gestão de autores, álbuns e músicas.
- Cálculo e consulta de direitos editoriais.
- Relatórios financeiros globais e individuais por autor.
- Pesquisa por autor, álbum ou música através do Whoosh.
- Reprodução de áudio através do Pygame.
- Registo de alterações através de snapshots dos dados.
- Consulta do histórico e reversão para estados anteriores.
- Armazenamento e gestão de dados em ficheiros CSV.
- Validação e pré-processamento dos dados de entrada.

## Tecnologias

| Tecnologia | Utilização |
| --- | --- |
| Python | Linguagem principal |
| Pygame | Reprodução de áudio |
| Whoosh | Indexação e pesquisa |
| pandas | Manipulação de dados |
| tabulate | Apresentação de tabelas na consola |
| schema | Validação de estruturas de dados |
| CSV | Armazenamento dos dados |

As dependências estão listadas em `requirements.txt`.

## Estrutura do código

```text
src/
├── BaseDados/
│   ├── fixDATA/
│   ├── dataSchema.py
│   └── getAudioPath.py
├── audio.py
├── crud.py
├── history.py
├── main.py
├── management.py
├── menu.py
├── reports.py
└── searchEngine.py
```

- `main.py`: ponto de entrada da aplicação.
- `menu.py`: menus e navegação na consola.
- `crud.py`: operações de criação, consulta, atualização e remoção.
- `management.py`: gestão de acesso e carregamento de dados.
- `reports.py`: relatórios financeiros.
- `searchEngine.py`: indexação e pesquisa com Whoosh.
- `audio.py`: reprodução de áudio.
- `history.py`: snapshots e reversão de alterações.
- `BaseDados/`: validação, preparação dos dados e construção de caminhos para áudio.

## Executar localmente

É necessário ter Python instalado.

1. Clonar o repositório.
2. Instalar as dependências:

```bash
pip install -r requirements.txt
```

3. Executar a aplicação a partir da raiz do projeto:

```bash
python src/main.py
```

A reprodução de áudio depende da existência dos ficheiros de música no formato e na estrutura de pastas esperados pela aplicação. Esta funcionalidade pode ser utilizada sem ficheiros de áudio, mas não será possível reproduzir músicas.

## Âmbito e estado

Este repositório documenta um projeto académico desenvolvido em grupo. A descrição das funcionalidades corresponde à estrutura e ao comportamento previstos no código do projeto; não constitui uma certificação de testes completos, segurança ou preparação para utilização em produção.

## Repositório

[13alves05/tocadiscos-editora](https://github.com/13alves05/tocadiscos-editora)
