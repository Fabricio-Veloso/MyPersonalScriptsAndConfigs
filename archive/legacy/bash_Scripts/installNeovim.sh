#!/bin/bash

# Atualizar pacotes
echo "[INFO] Atualizando pacotes..."
sudo apt update && sudo apt upgrade -y

# Instalar pre-requisitos
echo "[INFO] Instalando pre-requisitos para Neovim..."
sudo apt install -y software-properties-common git luarocks

# Adicionar repositorio e instalar Neovim
echo "[INFO] Adicionando repositorio oficial do Neovim..."
sudo add-apt-repository ppa:neovim-ppa/unstable -y
sudo apt update
sudo apt install -y neovim

# Preparar estrutura
echo "[INFO] Preparando estrutura de configuracao..."
mkdir -p ~/.config
rm -rf ~/.config/nvim

# Clonar configuracao
echo "[INFO] Clonando configuracoes do Fabricio para Neovim..."
git clone --depth 1 https://github.com/Fabricio-Veloso/nvim.git ~/.config/nvim

# Finalizacao
echo "[OK] Neovim instalado e configurado! Abra com 'nvim'."
