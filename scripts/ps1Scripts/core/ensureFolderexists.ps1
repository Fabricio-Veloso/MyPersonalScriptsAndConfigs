function Ensure-ProjectsFolder {
    $envType = Get-EnvironmentType

    # Determina a pasta base
    $basePath = if (Is-Windows) { $env:USERPROFILE } else { $env:HOME }

    if (-not (Test-Path $basePath)) {
        Write-Error "❌ Diretório base do usuário não encontrado: $basePath"
        exit 1
    }

    $projectsPath = Join-Path $basePath "projects"

    try {
        if (-not (Test-Path $projectsPath)) {
            New-Item -ItemType Directory -Path $projectsPath -Force | Out-Null
            Write-Host "✅ Pasta criada: $projectsPath"
        } else {
            Write-Host "📁 Pasta já existente: $projectsPath"
        }
    } catch {
        Write-Error "❌ Erro ao criar a pasta de projetos: $($_.Exception.Message)"
        exit 1
    }
}
