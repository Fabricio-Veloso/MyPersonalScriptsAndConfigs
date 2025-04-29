# 🛠 Setup de Ambiente com PowerShell e Bash

## Este projeto foi criado para automatizar a instalação de ferramentas essenciais para meu workflow como Neovim, obsidiane PowerShell em ambientes Windows, WSL e Linux puro.

- O foco principal é o PowerShell, usando scripts Bash apenas quando necessário (ex: preparar Linux puro).

📁 Estrutura de Pastas

MyPersonalscripts/
│
├── setup.ps1 # Script principal de automação (PowerShell)
│
├── bash/
└───│ Scripts de bash para linux puro(ex: Ubuntu)
│
└── README.md # Documentação do projeto

⚡ Como usar

### 1. Ambiente Windows/WSL

Se você está em Windows ou WSL, basta abrir o PowerShell como administrador e rodar:

Set-ExecutionPolicy Bypass -Scope Process -Force
.\ mainSetUpScript.ps1

Depois escolha uma das opções de acordo com o prompt para instalar os softwares disponíveis.

### 2. Ambiente Linux puro

Se você está em um Linux puro (Ubuntu, Debian, etc):
2.1 Primeiro passo: dar permissão aos scripts Bash

Depois de clonar o projeto, execute:

chmod +x bash/\*.sh

Isso garante que os scripts Bash possam ser executados.
2.2 Instalar PowerShell

Execute o script para instalar o PowerShell:

bash bash/install-pwsh.sh

Após instalado, inicie o PowerShell com:

pwsh

2.3 Rodar o mainSetUpScript.ps1 normalmente

Dentro do PowerShell, execute:

Set-ExecutionPolicy Bypass -Scope Process -Force
.\setup.ps1

🔥 Funções disponíveis no projeto

    Install-Neovim — Instala o Neovim via WSL (dentro do Linux do WSL).

    Install-NeovimPure — Instala o Neovim em um Linux nativo usando script Bash.

    Install-Git, Install-GoogleDrive, Install-Obsidian, Install-AutoHotkey, etc — outras funções de setup via PowerShell.

✅ Requisitos

    Acesso de sudo no Linux (para instalar pacotes)

    Permissões de execução para Bash (chmod +x bash/*.sh)

    Em Windows/WSL: PowerShell versão 5+ ou superior

    Em Linux: Instalar o PowerShell usando install-pwsh.sh

📌 Observações

    Sempre rode o setup.ps1 no contexto correto (Windows, WSL ou Linux puro).
    Todo o fluxo principal de automação acontece via PowerShell para centralizar a manutenção.
