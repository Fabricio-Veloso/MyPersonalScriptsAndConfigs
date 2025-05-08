#!/bin/bash

if ! command -v git &>/dev/null; then
  echo "[INFO] Git não encontrado. Instalando Git..."
  sudo apt update
  sudo apt install -y git
  echo "[OK] Git instalado com sucesso."
else
  echo "[OK] Git já está instalado."
fi
