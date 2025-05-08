
function Get-EnvironmentType {
    if ($env:OS -eq "Windows_NT") {
        return "Windows"
    }

    try {
        if (Test-Path -Path "/proc/version") {
            $versionInfo = Get-Content "/proc/version" -ErrorAction Stop
            if ($versionInfo -match "Microsoft") {
                return "WSL"
            }
        }
    } catch {}

    return "Linux"
}

