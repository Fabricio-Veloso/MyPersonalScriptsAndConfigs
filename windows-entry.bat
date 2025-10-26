
@echo off
setlocal

echo ----------------------------------------
echo  🚀 Iniciando setup do ambiente (Windows)
echo ----------------------------------------

REM Verifica se PowerShell 7 (pwsh) esta instalado
where pwsh >nul 2>nul
if %errorlevel% neq 0 (
    echo ⚠️ PowerShell 7 nao encontrado.
    set /p resp="Deseja instalar agora? (s/n): "
    if /I "%resp%"=="s" (
        echo 🔧 Instalando PowerShell 7 via winget...
        if exist "%ProgramFiles%\WindowsApps\Microsoft.DesktopAppInstaller*" (
            winget install --id Microsoft.PowerShell --source winget -e --accept-source-agreements --accept-package-agreements
            if %errorlevel% neq 0 (
                echo ❌ Erro ao tentar instalar o PowerShell. Encerrando.
                exit /b 1
            )
        ) else (
            echo ❌ Winget nao encontrado. Instale o App Installer manualmente.
            exit /b 1
        )
    ) else (
        echo ❌ Instalacao cancelada. Encerrando.
        exit /b 1
    )
)

echo ✅ PowerShell 7 encontrado. Executando script principal...
pwsh -File "%~dp0main.ps1"
endlocal
