#LINUX PURE(UBUNTU) FUNCTIONS NEED REFACTOR TO USE SYNCED WSL CLONED SCRIPTS AFTER THE SYNC UPDATE! 

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


