# Personal Environment Setup

CLI em Python para instalar, configurar e validar um ambiente pessoal de trabalho de forma reexecutavel, modular e multiplataforma.

## Direcao atual

- Python como orquestrador principal.
- Perfis declarativos para definir o ambiente desejado.
- Modulos por ferramenta ou capacidade.
- Adaptadores pequenos para diferencas de Windows e Linux.
- Fluxo principal baseado em `plan`, `apply`, `check` e `verify`.

## Estrutura inicial

- `src/personal_setup/` contem a CLI, modelos, servicos, modulos e adaptadores.
- `profiles/` guarda a composicao declarativa do ambiente.
- `assets/` guarda configuracoes versionadas do ambiente.
- `tests/` contem testes pequenos da base da aplicacao.
- `docs/specs/` e `docs/decisions/` guardam specs curtas e decisoes estaveis.

## Fluxo esperado

- `plan`: compara estado atual e estado desejado.
- `apply`: executa as mudancas necessarias.
- `check`: mostra o estado atual por modulo.
- `verify`: valida se o resultado final ficou funcional.

## Estado atual da base

- `full.toml` ja inclui `git`, `project_folders`, `neovim`, `autohotkey` e `glazewm`.
- `project_folders` ja usa o nome configurado pelo usuario para resolver o caminho no Windows.
- `autohotkey` ja valida instalacao, script em `Documents` e script na pasta de `Startup`.
- `glazewm` ja valida instalacao, config versionada e atalho de inicializacao com o sistema.

## Estado do repositorio

Esta e a fundacao da nova arquitetura do projeto. Os scripts antigos ainda podem servir como referencia de comportamento e ativos a migrar, mas a direcao principal agora parte da CLI em Python.

## Como executar

Hoje voce ja pode iniciar a CLI local com um unico comando:

```bash
python main.py
```

Ao iniciar sem argumentos, a CLI mostra um menu com as opcoes disponiveis, incluindo configurar o nome do usuario, planejar, aplicar, checar e verificar o ambiente.

Se preferir executar de forma direta, a base tambem suporta comandos como:

```bash
python main.py plan --profile full
python main.py apply --profile full
python main.py configure-user --name Fabricio
```
