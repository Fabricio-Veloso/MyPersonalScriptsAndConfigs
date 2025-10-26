# IMPORTS
. "$PSScriptRoot\scripts\ps1Scripts\windows\ensure-GitInstalled.ps1"
. "$PSScriptRoot\scripts\ps1Scripts\windows\install-WithWinget.ps1"
. "$PSScriptRoot\scripts\ps1Scripts\windows\install-AutoHotkey.ps1"
. "$PSScriptRoot\scripts\ps1Scripts\wsl\install-WSL-Dependencies.ps1"
. "$PSScriptRoot\scripts\ps1Scripts\wsl\install-NeovimWSL.ps1"
. "$PSScriptRoot\scripts\ps1Scripts\core\getEnvironmentType.ps1"
. "$PSScriptRoot\scripts\ps1Scripts\core\write-ColeredMesage.ps1"
. "$PSScriptRoot\scripts\ps1Scripts\core\startInstaller.ps1"
. "$PSScriptRoot\scripts\ps1Scripts\windows\configure-GlazeWM.ps1"

#VARS
$UserName = "Fabricio"
# $desktopPath = [Environment]::GetFolderPath("Desktop")
# $DeskTopUserFolder = Join-Path $desktopPath $UserName
$ProjectFolderPath = "\projetos"
$RepoFolderName = "MyPersonalScriptsAndConfigs"
$ScriptsAndConfigsRepoPath = Join-Path $ProjectFolderPath $RepoFolderName
$repoAHK = "https://github.com/Fabricio-Veloso/MyPersonalScriptsAndConfigs.git"
$scriptAHK = Join-Path $ScriptsAndConfigsRepoPath "scripts\autoHotKeyScripts\mainScript.ahk"


if (-not (Test-Path $projectsPath)) {
    New-Item -ItemType Directory -Path $projectsPath -Force | Out-Null
    Write-Host "✅ Pasta criada: $projectsPath"
} else {
    Write-Host "📁 Pasta já existente: $projectsPath"
}

#Stars-Sleep -Seconds 50
# Iniciar o script
Start-Installer

