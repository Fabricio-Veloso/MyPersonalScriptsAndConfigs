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
    if (-not (Test-Path $ScriptsAndConfigsRepoPath)) {
      git clone $repoAHK $ScriptsAndConfigsRepoPath
      Write-Host "[OK] Repositorio clonado em: $ScriptsAndConfigsRepoPath"
    } else {
      Write-Host "[INFO] Repositório já existe em: $ScriptsAndConfigsRepoPath. Atualizando..."
      Push-Location $ScriptsAndConfigsRepoPath
      git pull
      Pop-Location   
    }

    $executar = Read-Host "Deseja ativar o script AutoHotkey agora? (y/n)"
    if ($executar -eq 'y') {
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

