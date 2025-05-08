. "$PSScriptRoot\..\core\write-ColoredMesage.ps1"
function configure-GlazeWM {
    param (
        [string]$CustomConfigPath = "$PSScriptRoot..\..\..\..\configs\glazeWM\config.yaml"
    )

    # Check if GlazeWM is installed
    $glazeInstalled = Get-Command "glazewm" -ErrorAction SilentlyContinue

    
    if ($glazeInstalled) {

        $glazeConfigDir = Join-Path $env:USERPROFILE ".glzr\glazewm"

        if (-not (Test-Path $glazeConfigDir)) {
            Write-ColoredMessage "Failed to find configuration directory: $glazeConfigDir" "Red"
            Start-Process "glazewm"
            Start-Sleep -Seconds 5
            Stop-Process -Name "glazewm" -Force -ErrorAction SilentlyContinue
        }
       
        try {
        Copy-Item -Path $CustomConfigPath -Destination "$glazeConfigDir\config.yaml" -Force
        Write-ColoredMessage "Configuration copied to GlazeWM folder." "Green"
        } catch {
            Write-ColoredMessage "Failed to copy configuration file: $_" "Red"
            return
        } 
        
       # Ask about startup, only if not already set
       $startupFolder = [Environment]::GetFolderPath("Startup")
       $shortcutPath = Join-Path $startupFolder "GlazeWM.lnk"

       if (Test-Path $shortcutPath) {
            Write-ColoredMessage "GlazeWM is already set to start with Windows." "Blue"
       } else {
           $answer = Read-Host "Do you want GlazeWM to start with Windows? (y/n)"
           if ($answer -eq 'y') {
                $glazePath = (Get-Command "glazewm").Source

               try {
                   $wshShell = New-Object -ComObject WScript.Shell
                   $shortcut = $wshShell.CreateShortcut($shortcutPath)
                   $shortcut.TargetPath = $glazePath
                   $shortcut.Save()
                   Write-ColoredMessage "GlazeWM will start with Windows." "Green"
               } catch {
                   Write-ColoredMessage "Failed to create startup shortcut: $_" "Red"
               }
           } else {
               Write-ColoredMessage "Startup option skipped." "Blue"
           }
       }

       Start-Process "glazewm"

    }else {
        Write-ColoredMessage "GlazeWM is not installed thefore cant be configured" "red"
        return
    }      

}


