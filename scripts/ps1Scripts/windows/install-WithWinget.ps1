. "$PSScriptRoot\..\core\write-ColoredMesage.ps1"

function Install-WithWinget {
    param (
        [string]$packageName,   # Nome do pacote no winget
        [string]$displayName    # Nome legível do app
    )

    Write-ColoredMesage "`n[INFO] Iniciando novo terminal para instalar $displayName..." "Blue"

    $command = "winget install $packageName --silent --accept-package-agreements --accept-source-agreements; Exit"

    Start-Process "powershell.exe" -ArgumentList "-NoExit", "-Command", $command
}







function Install-Git          { Install-WithWinget "Git.Git" "Git" }
function Install-GoogleDrive  { Install-WithWinget "Google.Drive" "Google Drive" }
function Install-Obsidian     { Install-WithWinget "Obsidian.Obsidian" "Obsidian" }
function Install-GlazeWM      { Install-WithWinget "GlazeWM" "GlazeWM" }


