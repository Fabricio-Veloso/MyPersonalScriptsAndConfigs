# Verificar se Git esta instalado
function Ensure-GitInstalled {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host "[INFO] Git nao encontrado. Instalando Git..."
        Install-Git
    } else {
        Write-Host "[OK] Git ja esta instalado."
    }
}

