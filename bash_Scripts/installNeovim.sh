#!/bin/bash

# Atualizar pacotes
echo "[INFO] Atualizando pacotes..."
sudo apt update && sudo apt upgrade -y

# Instalar pré-requisitos
echo "[INFO] Instalando pré-requisitos para Neovim..."
sudo apt install -y software-properties-common git luarocks

# Adicionar repositório e instalar Neovim
echo "[INFO] Adicionando repositório oficial do Neovim..."
sudo add-apt-repository ppa:neovim-ppa/unstable -y
sudo apt update
sudo apt install -y neovim

# Preparar estrutura
echo "[INFO] Preparando estrutura de configuração..."
mkdir -p ~/.config
rm -rf ~/.config/nvim

# Clonar configuração
echo "[INFO] Clonando configurações do Fabricio para Neovim..."
git clone --depth 1 https://github.com/Fabricio-Veloso/nvim.git ~/.config/nvim

# Finalização
echo "[OK] Neovim instalado e configurado! Abra com 'nvim'."
