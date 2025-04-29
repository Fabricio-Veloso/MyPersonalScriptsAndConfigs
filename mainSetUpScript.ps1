# Variaveis personalizaveis
$nomeUsuario = "Fabricio"
$desktopPath = [Environment]::GetFolderPath("Desktop")
$caminhoBase = Join-Path $desktopPath $nomeUsuario
$caminhoProjetos = "$caminhoBase\projetos"
$caminhoRepoAHK = "$caminhoBase\MyPersonalScripts"
$repoAHK = "https://github.com/Fabricio-Veloso/MyPersonalScripts.git"

#SCRIPT SETUP FUNCTIONS

# Funcao principal
function Start-Installer {
    $envType = Get-EnvironmentType

    # Define menu de forma ordenada por ambiente
    $menuOptions = @()

    switch ($envType) {
        "Linux" {
            $menuOptions += @{ Key = 1; Label = "Instalar Neovim (Linux Puro)"; Action = { Install-NeovimPure } }
            $menuOptions += @{ Key = 2; Label = "Sair"; Action = { return $true } }
        }
        "Windows" 
        {
            $menuOptions += @{ Key = 1; Label = "Instalar Neovim"; Action = { Install-NeovimWSL } }
            $menuOptions += @{ Key = 2; Label = "Instalar Git"; Action = { Install-Git } }
            $menuOptions += @{ Key = 3; Label = "Instalar Google Drive"; Action = { Install-GoogleDrive } }
            $menuOptions += @{ Key = 4; Label = "Instalar Obsidian"; Action = { Install-Obsidian } }
            $menuOptions += @{ Key = 5; Label = "Instalar AutoHotkey"; Action = { Install-AutoHotkey } }
            $menuOptions += @{ Key = 6; Label = "Instalar dependências do WSL"; Action = { Install-WSL-Dependencies } }
            $menuOptions += @{ Key = 7; Label = "Instalar tudo"; Action = { Install-All } }
            $menuOptions += @{ Key = 8; Label = "Sair"; Action = { return $true } }
        }
    }

    $exit = $false
    while (-not $exit) {
        Clear-Host
        Write-Host "===== Menu de Instalacao ($envType) ====="
        
        foreach ($item in $menuOptions | Sort-Object { [int]$_.Key }) {
            Write-Host "$($item.Key). $($item.Label)"
        }

        $choice = Read-Host "Escolha uma opcao"
        $selected = $menuOptions | Where-Object { $_.Key -eq [int]$choice }

        if ($null -ne $selected) {
            $shouldExit = & $selected.Action
            if ($shouldExit) {
                Write-Host "`n[INFO] Saindo..."
                $exit = $true
            }
        } else {
            Write-Host "[ERRO] Opcao invalida. Tente novamente."
        }

        if (-not $exit) {
            Pause
        }
    }
}

# Environment check
function Get-EnvironmentType {
    if ($env:OS -eq "Windows_NT") {
        return "Windows"
    }

    try {
        if (Test-Path -Path "/proc/version") {
            $versionInfo = Get-Content "/proc/version" -ErrorAction Stop
            if ($versionInfo -match "Microsoft") {
                return "WSL"
            }
        }
    } catch {}

    return "Linux"
}

# Criar pastas iniciais
if (-not (Test-Path $caminhoProjetos)) {
    New-Item -ItemType Directory -Path $caminhoProjetos -Force | Out-Null
    Write-Host "[OK] Pasta '$caminhoProjetos' criada."
}

#WINDOS/WSL FUNCTIONS

# Usar winget para instalar um pacote
function Install-WithWinget($packageId, $nomeApp) {
    Write-Host "`n[INFO] Instalando $nomeApp..."
    winget install --id $packageId --silent --accept-package-agreements --accept-source-agreements
    Write-Host "[OK] $nomeApp instalado com sucesso.`n"
}

# Verificar se Git esta instalado
function Ensure-GitInstalled {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host "[INFO] Git nao encontrado. Instalando Git..."
        Install-Git
    } else {
        Write-Host "[OK] Git ja esta instalado."
    }
}

# Instala neovim no wsl
function Install-NeovimWSL       {
    Install-WSL-Dependencies
    
    echo 'Instalando Neovim' 
    # Adicionar repositório oficial do Neovim
    sudo apt install -y software-properties-common
    sudo add-apt-repository ppa:neovim-ppa/unstable -y
    sudo apt update
    sudo apt install -y neovim

    echo 'Instalando Luarocks...'
    sudo apt install -y luarocks

    echo 'Preparando estrutura do Neovim...'
    mkdir -p ~/.config
    rm -rf ~/.config/nvim

    echo 'Clonando configuração do usuário Fabricio...'
    git clone --depth 1 https://github.com/Fabricio-Veloso/nvim.git ~/.config/nvim
    echo 'Setup finalizado! Agora é só abrir o nvim :)'
}

# Instalacao com winget
function Install-Git          { Install-WithWinget "Git.Git" "Git" }
function Install-GoogleDrive  { Install-WithWinget "Google.Drive" "Google Drive" }
function Install-Obsidian     { Install-WithWinget "Obsidian.Obsidian" "Obsidian" }

# Instalar e configurar AutoHotkey
function Install-AutoHotkey {
    # Verifica se o AutoHotkey está instalado

    $ahkInstalled = Get-Command "AutoHotkey64.exe" -ErrorAction SilentlyContinue

    if (-not $ahkInstalled) {
        Install-WithWinget "AutoHotkey.AutoHotkey" "AutoHotkey"
    } else {
        Write-Host "[OK] AutoHotkey já está instalado."
    }

    $configurar = Read-Host "Deseja configurar o AutoHotkey com sua configuracao padrao? (y/n)"
    if ($configurar -eq 'y') {
        Ensure-GitInstalled
        if (-not (Test-Path $caminhoRepoAHK)) {
            git clone $repoAHK $caminhoRepoAHK
            Write-Host "[OK] Repositorio clonado em: $caminhoRepoAHK"
        } else {
            Write-Host "[INFO] Repositorio ja existe em: $caminhoRepoAHK"
        }

        $executar = Read-Host "Deseja ativar o script AutoHotkey agora? (y/n)"
        if ($executar -eq 'y') {
            $scriptAHK = Join-Path $caminhoRepoAHK "testescript.ahk"
          if (Test-Path $scriptAHK) {
              Start-Process $scriptAHK
              Write-Host "[OK] Script AHK executado diretamente."
          } else {
              Write-Host "[ERRO] Script AHK não encontrado em '$scriptAHK'."
          }

        }

        $iniciarComSistema = Read-Host "Deseja adicionar o script AHK na inicialização do sistema? (y/n)"
        if ($iniciarComSistema -eq 'y') {
            $startupFolder = [Environment]::GetFolderPath("Startup")
            $atalhoPath = Join-Path $startupFolder "AutoHotkey - Meu Script.lnk"
            $wshell = New-Object -ComObject WScript.Shell
            $shortcut = $wshell.CreateShortcut($atalhoPath)
            $shortcut.TargetPath = $scriptAHK
            $shortcut.Save()
            Write-Host "[OK] Script AHK adicionado na inicialização com o nome 'AutoHotkey - Meu Script'."
        }
    }}

# Instalar dependencias dentro do WSL
function Install-WSL-Dependencies {
    Write-Host "`n[INFO] Instalando dependencias do WSL..."
    wsl sudo apt update
    wsl sudo apt install -y git curl build-essential
    Write-Host "[OK] Dependencias do WSL instaladas.`n"
}

# Instalar tudo
function Install-All {
    Install-Neovim
    Install-Git
    Install-GoogleDrive
    Install-Obsidian
    Install-AutoHotkey
    Install-WSL-Dependencies
    Write-Host "`n[OK] Todos os programas foram instalados com sucesso!"
}


#LINUX PURE(UBUNTU) FUNCTIONS

# Calls bash script to install neovim on ubuntu
function Install-NeovimPure {
    & bash ./bash_Scripts/installNeovim.sh
}


# Calls bash script to install git on ubuntu
function Ensure-GitInstalledPure {
    & bash ./bash_Scripts/ensureGitInstalled.sh
}

# Calls bash script to ensure the presense on my default working directories on ubuntu
function Ensure-DefaultDirectoryStructurePure {
    & bash ./scripts/createDefaultDirectoryStructure.sh
}

# Calls bash script to add the alias to my project folder and start nvim
function Add-ProjectAlias-Linux {
    $scriptPath = "./bash_Scripts/createAlias.sh"
    if (Test-Path $scriptPath) {
        bash $scriptPath
    } else {
        Write-Host "[ERRO] Script '$scriptPath' não encontrado."
    }
}


# Iniciar o script
Start-Installer

