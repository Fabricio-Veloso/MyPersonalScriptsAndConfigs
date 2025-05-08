#!/bin/bash

# Define o comando do alias para abrir a pasta ~/projects com nvim
ALIAS_CMD="alias pj='cd ~/projects && nvim'"

# Verifica se o alias já existe
if ! grep -Fxq "$ALIAS_CMD" ~/.bash_aliases; then
  echo "$ALIAS_CMD" >>~/.bash_aliases
  echo "[OK] Alias 'pj' adicionado ao ~/.bash_aliases."
else
  echo "[INFO] Alias 'pj' já existe em ~/.bash_aliases."
fi

echo "[INFO] Reinicie o terminal WSL para o alias funcionar."
