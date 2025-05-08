function Start-Installer {
    $envType = Get-EnvironmentType

    # Define menu de forma ordenada por ambiente
    $menuOptions = @()

    switch ($envType) {
        "Linux" {
            $menuOptions += @{ Key = 1; Label = "Install Neovim (Pure Linux)"; Action = { Install-NeovimPure } }
            $menuOptions += @{ Key = 2; Label = "Exit"; Action = { return $true } }
        }
        "Windows" {
            $menuOptions += @{ Key = 1; Label = "Install And Configure Neovim"; Action = { install-NeovimWSL } }
            $menuOptions += @{ Key = 2; Label = "Install Git"; Action = { Install-Git } }
            $menuOptions += @{ Key = 3; Label = "Install Google Drive"; Action = { Install-GoogleDrive } }
            $menuOptions += @{ Key = 4; Label = "Install Obsidian"; Action = { Install-Obsidian } }
            $menuOptions += @{ Key = 5; Label = "Install And Configure AutoHotkey"; Action = { Install-AutoHotkey } }
            $menuOptions += @{ Key = 6; Label = "Install WSL Dependencies"; Action = { Install-WSL-Dependencies } }
            $menuOptions += @{ Key = 7; Label = "Install GlazeWM"; Action = { Install-GlazeWM} }
            $menuOptions += @{ Key = 8; Label = "Configure GlazeWM"; Action = {configure-GlazeWM } }
            $menuOptions += @{ Key = 9; Label = "Exit"; Action = { return $true } }
        }
    }

    $exit = $false
    while (-not $exit) {
        Clear-Host
        Write-Host "===== Environment installer:($envType) ====="
        
        foreach ($item in $menuOptions | Sort-Object { [int]$_.Key }) {
            Write-Host "$($item.Key). $($item.Label)"
        }

        $choice = Read-Host "pick an option"
        $selected = $menuOptions | Where-Object { $_.Key -eq [int]$choice }

        if ($null -ne $selected) {
            $shouldExit = & $selected.Action
            if ($shouldExit) {
                Write-Host "`n[INFO] exiting..."
                $exit = $true
            }
        } else {
            Write-Host "[ERROR] Invalid Option ."
        }

        if (-not $exit) {
            Pause
        }
    }
}


