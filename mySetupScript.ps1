# Variaveis personalizaveis
$nomeUsuario = "Fabricio"
$desktopPath = [Environment]::GetFolderPath("Desktop")
$caminhoBase = Join-Path $desktopPath $nomeUsuario
$caminhoProjetos = "$caminhoBase\projetos"
$caminhoRepoAHK = "$caminhoBase\MyPersonalScripts"
$repoAHK = "https://github.com/Fabricio-Veloso/MyPersonalScripts.git"

# Criar pastas iniciais
if (-not (Test-Path $caminhoProjetos)) {
    New-Item -ItemType Directory -Path $caminhoProjetos -Force | Out-Null
    Write-Host "[OK] Pasta '$caminhoProjetos' criada."
}

# Funcao para exibir o menu de opcoes
function Show-Menu {
    Clear-Host
    Write-Host "========================================="
    Write-Host "   Bem-vindo ao instalador do setup"
    Write-Host "========================================="
    Write-Host "Escolha uma opcao:"
    Write-Host "1. Instalar Neovim"
    Write-Host "2. Instalar Git"
    Write-Host "3. Instalar Google Drive"
    Write-Host "4. Instalar Obsidian"
    Write-Host "5. Instalar e configurar AutoHotkey"
    Write-Host "6. Instalar dependencias do WSL"
    Write-Host "7. Instalar tudo"
    Write-Host "8. Sair"
    Write-Host "========================================="
}

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

# Instalacao com winget
function Install-Neovim       { Install-WithWinget "Neovim.Neovim" "Neovim" }
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

    $configurar = Read-Host "Deseja configurar o AutoHotkey com sua configuração padrão? (y/n)"
    if ($configurar -eq 'y') {
        Ensure-GitInstalled
        if (-not (Test-Path $caminhoRepoAHK)) {
            git clone $repoAHK $caminhoRepoAHK
            Write-Host "[OK] Repositório clonado em: $caminhoRepoAHK"
        } else {
            Write-Host "[INFO] Repositório já existe em: $caminhoRepoAHK"
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

# Funcao principal
function Start-Installer {
    $exit = $false
    while (-not $exit) {
        Show-Menu
        $choice = Read-Host "Escolha uma opcao (1 a 8)"

        switch ($choice) {
            '1' { Install-Neovim }
            '2' { Install-Git }
            '3' { Install-GoogleDrive }
            '4' { Install-Obsidian }
            '5' { Install-AutoHotkey }
            '6' { Install-WSL-Dependencies }
            '7' { Install-All }
            '8' {
                Write-Host "[INFO] Saindo..."
                $exit = $true
            }
            default { Write-Host "[ERRO] Opcao invalida. Tente novamente." }
        }

        if (-not $exit) {
            Pause
        }
    }
}

# Iniciar o script
Start-Installer

