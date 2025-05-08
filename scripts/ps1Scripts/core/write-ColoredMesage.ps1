Function write-ColoredMesage {
    param (
        [string]$Message,
        [ValidateSet("Red", "Green", "Blue", "Yellow", "Cyan", "White", "Gray")]
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

