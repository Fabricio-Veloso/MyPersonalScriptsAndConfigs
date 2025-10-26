
# -----------------------------
# 1. Função para identificar o ambiente
# -----------------------------
function Get-EnvironmentType {
    try {
        if ($env:OS -eq "Windows_NT") {
            return "Windows"
        }

        if (Test-Path -Path "/proc/version") {
            $versionInfo = Get-Content "/proc/version" -ErrorAction Stop
            if ($versionInfo -match "microsoft") {
                return "WSL"
            }
        }

        return "Linux"
    }
    catch {
        return "Desconhecido"
    }
}

# -----------------------------
# 2. Função auxiliar para saber se é Windows
# -----------------------------
function Is-Windows {
    return (Get-EnvironmentType) -eq "Windows"
}

# -----------------------------
# 3. Checagem se PowerShell está instalado
# -----------------------------
function Ensure-PowerShellInstalled {
    param(
        [switch]$Silent
    )

    # Detecta se já está no PowerShell Core (pwsh)
    if ($PSVersionTable.PSEdition -eq "Core" -or (Get-Command pwsh -ErrorAction SilentlyContinue)) {
        if (-not $Silent) { Write-Host "✅ PowerShell já está instalado e acessível." }
        return $true
    }

    # Caso não esteja instalado, oferece a opção de instalar
    if (-not $Silent) {
        Write-Host "⚠️  PowerShell não foi encontrado no sistema."
        $resp = Read-Host "Deseja tentar instalar agora? (s/n)"
        if ($resp -ne 's' -and $resp -ne 'S') {
            Write-Host "Instalação cancelada. Encerrando script."
            exit 1
        }
    }

    $envType = Get-EnvironmentType
    try {
        switch ($envType) {
            "Windows" {
                Write-Host "🔧 Instalando PowerShell via winget..."
                if (Get-Command winget -ErrorAction SilentlyContinue) {
                    winget install --id Microsoft.PowerShell --source winget -e --accept-source-agreements --accept-package-agreements
                } else {
                    Write-Error "❌ Winget não encontrado. Instale-o manualmente antes de continuar."
                    exit 1
                }
            }

            "Linux" {
                Write-Host "🔧 Instalando PowerShell via pacote do sistema..."
                if (Get-Command apt -ErrorAction SilentlyContinue) {
                    sudo apt update && sudo apt install -y powershell
                } elseif (Get-Command dnf -ErrorAction SilentlyContinue) {
                    sudo dnf install -y powershell
                } elseif (Get-Command pacman -ErrorAction SilentlyContinue) {
                    sudo pacman -Syu --noconfirm powershell
                } else {
                    Write-Error "❌ Não foi possível determinar o gerenciador de pacotes."
                    exit 1
                }
            }

            "WSL" {
                Write-Host "🔧 Instalando PowerShell dentro do WSL (mesmo procedimento do Linux)..."
                sudo apt update && sudo apt install -y powershell
            }

            Default {
                Write-Error "❌ Ambiente desconhecido. Não foi possível instalar automaticamente."
                exit 1
            }
        }
    } catch {
        Write-Error "❌ Falha ao tentar instalar PowerShell: $($_.Exception.Message)"
        exit 1
    }

    Write-Host "✅ PowerShell instalado com sucesso."
    return $true
}

# -----------------------------
# 4. Cria a pasta "projects"
# -----------------------------
function Ensure-ProjectsFolder {
    $envType = Get-EnvironmentType

    # Determina a pasta base
    $basePath = if (Is-Windows) { $env:USERPROFILE } else { $env:HOME }

    if (-not (Test-Path $basePath)) {
        Write-Error "❌ Diretório base do usuário não encontrado: $basePath"
        exit 1
    }

    $projectsPath = Join-Path $basePath "projects"

    try {
        if (-not (Test-Path $projectsPath)) {
            New-Item -ItemType Directory -Path $projectsPath -Force | Out-Null
            Write-Host "✅ Pasta criada: $projectsPath"
        } else {
            Write-Host "📁 Pasta já existente: $projectsPath"
        }
    } catch {
        Write-Error "❌ Erro ao criar a pasta de projetos: $($_.Exception.Message)"
        exit 1
    }
}

# -----------------------------
# Execução principal
# -----------------------------
Write-Host "------------------------------------"
Write-Host "🧭 Iniciando verificação do ambiente..."
Write-Host "------------------------------------"

$envType = Get-EnvironmentType
Write-Host "🌐 Ambiente detectado: $envType"

Ensure-PowerShellInstalled
Ensure-ProjectsFolder
Write-Host "✅ Script finalizado com sucesso."
