# Tocadiscos Editora

Projeto académico de grupo desenvolvido no âmbito da unidade curricular de Algoritmos e Programação, no curso de Desenvolvimento de Software, durante o ano letivo de 2025/2026.

A aplicação é executada na linha de comandos (CLI) e permite gerir o catálogo de uma editora musical fictícia. O sistema trabalha com autores, álbuns e músicas, calcula direitos editoriais, disponibiliza pesquisa, permite reproduzir ficheiros de áudio e mantém um histórico de alterações com possibilidade de reversão.

## Autoria e colaboração

Projeto desenvolvido por quatro elementos:

- Bruno Oliveira
- Gabriela Tavares
- Leonardo Alves
- Vinicius Toniato

Leonardo Alves e Bruno Oliveira tiveram a participação mais expressiva no desenvolvimento. Gabriela Tavares e Vinicius Toniato também integraram o grupo e contribuíram para o trabalho.

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

3. Criar o administrador local com o comando indicado na secção seguinte.
4. Executar a aplicação a partir da raiz do projeto:

```bash
python src/main.py
```

### Criar utilizadores administradores

Depois de instalar as dependências, cria o ficheiro local de administradores:

```bash
python src/setup_admins.py
```

O assistente pede o nome de utilizador e uma palavra-passe com pelo menos 12 caracteres. O ficheiro `data/admins.csv` é criado apenas na máquina local e está excluído do Git. Para uma instalação nova, este passo é necessário antes de utilizar as opções protegidas por autenticação.

A reprodução de áudio depende da existência dos ficheiros de música no formato e na estrutura de pastas esperados pela aplicação. Sem esses ficheiros, as restantes funcionalidades podem ser exploradas, mas não será possível reproduzir músicas.

## Limitações e segurança

Este projeto foi desenvolvido para fins académicos e não deve ser utilizado como sistema de gestão real ou exposto como serviço público.

- As palavras-passe dos administradores são verificadas através de PBKDF2-HMAC-SHA256 com salt individual e 260 000 iterações.
- As credenciais locais são guardadas em `data/admins.csv`, ficheiro excluído do Git. O repositório não deve conter palavras-passe, hashes de produção ou credenciais pessoais.
- As credenciais que constavam de versões anteriores do repositório foram publicadas no histórico Git. Devem ser consideradas comprometidas e substituídas; remover o ficheiro da versão atual não apaga os commits antigos.
- A autenticação continua a ser uma implementação académica simples e não substitui um sistema de gestão de utilizadores com controlo de sessões, limitação de tentativas e auditoria.
- Não existe uma suite de testes automatizados no repositório. As funcionalidades devem ser verificadas manualmente.
- As dependências de `requirements.txt` não têm versões fixas, pelo que a instalação pode produzir ambientes diferentes ao longo do tempo.
- O histórico de alterações é baseado em cópias locais dos ficheiros CSV e não substitui uma estratégia de cópias de segurança testada.

## Âmbito e estado

Este repositório documenta um projeto académico desenvolvido em grupo. A descrição das funcionalidades corresponde à estrutura e ao comportamento identificados no código; não constitui uma certificação de testes completos, segurança ou preparação para utilização em produção.

## Repositório

[13alves05/tocadiscos-editora](https://github.com/13alves05/tocadiscos-editora)
