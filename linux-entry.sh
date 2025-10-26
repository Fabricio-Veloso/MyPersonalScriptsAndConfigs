
#!/usr/bin/env bash
set -e

echo "----------------------------------------"
echo " 🚀 Iniciando setup do ambiente (Linux)"
echo "----------------------------------------"

if ! command -v pwsh &> /dev/null; then
  echo "⚠️  PowerShell 7 não encontrado."
  read -p "Deseja instalar agora? (s/n): " resp
  if [[ "$resp" =~ ^[sS]$ ]]; then
    echo "🔧 Instalando PowerShell 7..."
    if command -v apt &> /dev/null; then
      sudo apt update && sudo apt install -y powershell
    elif command -v dnf &> /dev/null; then
      sudo dnf install -y powershell
    elif command -v pacman &> /dev/null; then
      sudo pacman -Syu --noconfirm powershell
    else
      echo "❌ Não foi possível detectar o gerenciador de pacotes."
      exit 1
    fi
  else
    echo "❌ Instalação cancelada."
    exit 1
  fi
fi

echo "✅ PowerShell 7 encontrado. Executando script principal..."
pwsh "$PWD/main.ps1"
