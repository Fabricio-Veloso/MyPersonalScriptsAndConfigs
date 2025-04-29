#!/bin/bash

CAMINHO_PROJETOS="/home/$USER/Projetos"

if [ ! -d "$CAMINHO_PROJETOS" ]; then
  mkdir -p "$CAMINHO_PROJETOS"
  echo "[OK] Pasta '$CAMINHO_PROJETOS' criada."
else
  echo "[OK] Pasta '$CAMINHO_PROJETOS' já existe."
fi
