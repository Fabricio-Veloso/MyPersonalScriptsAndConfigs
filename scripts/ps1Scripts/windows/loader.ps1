# Inicializa status de importação
$ImportStatus = @{ Success = $true; Errors = @() }

Write-Host "`n== Loading script functions ==" -ForegroundColor Blue

function Import-ScriptFile {
param ([string]$Path)

  if (-not (Test-Path $Path)) {
    $ImportStatus.Errors += " File not found: $Path"
    $ImportStatus.Success = $false
    return
  }

  try {
    . $Path
  } catch {
    $ImportStatus.Errors += " Failed to import: $Path - $_"
    $ImportStatus.Success = $false
  }
}

# Lista de scripts a importar
$scriptPaths = @(
  "$PSScriptRoot\ensure-GitInstalled.ps1",
  "$PSScriptRoot\install-WithWinget.ps1",
  "$PSScriptRoot\install-AutoHotkey.ps1",
  "$PSScriptRoot\..\wsl\install-WSL-Dependencies.ps1",
  "$PSScriptRoot\..\wsl\install-NeovimWSL.ps1"
)

# Importa todos
foreach ($script in $scriptPaths) {
  Import-ScriptFile $script
}

# Exibe falhas (se houver)
if (-not $ImportStatus.Success) {
  Write-Host "`n[ERROR] Some imports failed:" -ForegroundColor Red
  foreach ($err in $ImportStatus.Errors) {
    Write-Host $err -ForegroundColor Red
  }
}

