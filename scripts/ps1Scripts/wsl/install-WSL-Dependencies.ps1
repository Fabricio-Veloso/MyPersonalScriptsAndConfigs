# Instalar dependencias dentro do WSL
function Install-WSL-Dependencies {
    Write-Host "`n[INFO] Installing WSL build-essential..."
    wsl sudo apt update
    wsl sudo apt install -y git curl build-essential
    Write-Host "[OK] Dependencies installed.`n"
}

