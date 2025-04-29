#!/bin/bash

# Atualizar pacotes
echo "[INFO] Atualizando pacotes..."
sudo apt update && sudo apt upgrade -y

# Instalar pré-requisitos
echo "[INFO] Instalando dependências necessárias..."
sudo apt install -y wget apt-transport-https software-properties-common

# Baixar e registrar repositório do PowerShell
echo "[INFO] Registrando repositório do PowerShell..."
wget -q "https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb" -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb

# Atualizar de novo e instalar o PowerShell
echo "[INFO] Instalando PowerShell..."
sudo apt update
sudo apt install -y powershell

# Finalização
echo "[OK] PowerShell instalado com sucesso! Execute 'pwsh' para começar."
