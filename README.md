# 🛠 Setup de Ambiente com PowerShell e Bash

- Este projeto foi criado para automatizar a instalação de ferramentas essenciais para meu workflow como Neovim, obsidiane PowerShell em ambientes Windows, WSL e Linux puro.

- O foco principal é o PowerShell, usando scripts Bash apenas quando necessário.

📁 Estrutura de Pastas

MyPersonalscripts/ │ ├── setup.ps1 # Script principal de automação (PowerShell) │ ├── bash/ └───│ Scripts de bash para linux puro(ex: Ubuntu) │ └── README.md # Documentação do projeto

✅ Requisitos

- Acesso de sudo no Linux (para instalar pacotes)

- Permissões de execução para Bash (chmod +x bash/\*.sh)

- Em Windows/WSL: PowerShell versão 5+ ou superior

- Em Linux: Instalar o PowerShell usando install-pwsh.sh

## Como usar

### 1.Powershell para interagir com WSL e windows.

Dentro do PowerShell, execute:

```
Set-ExecutionPolicy Bypass -Scope Process -Force .\setup.ps1
```

🔥 Funções disponíveis no projeto

- Instalar:
  - WSL(windows).
  - Obsidian(windows).
  - google drive(windows).
  - Autohotkey(windows).
  - git(windows e wsl).
  - Neovim(wsl).
- Configurar
  - Autohotkey(wsl).
  - Neovim(wsl).
  - Minha estrutura padrão de pastas de projetos.

### 2. Ambiente Linux puro

_Se você está em um Linux puro (Ubuntu, Debian, etc): 2.1 Primeiro passo: dar permissão aos scripts Bash_

Depois de clonar o projeto, execute:

```
chmod +x bash/*.sh
```

Isso garante que os scripts Bash possam ser executados. 2.2 Instalar PowerShell

Execute o script para instalar o PowerShell:

```
bash bash/install-pwsh.sh
```

Após instalado, inicie o PowerShell com:

```
pwsh
```

2.3 Rodar o mainSetUpScript.ps1 normalmente. Dentro do PowerShell, execute:

```
Set-ExecutionPolicy Bypass -Scope Process -Force .\setup.ps1
```

📌 Observações
_Os scripts de bash para env linux puro (ubuntu) ainda não foram testados_
