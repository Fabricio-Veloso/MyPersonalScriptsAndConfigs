#!/bin/bash

ALIAS_NAME="p"
ALIAS_COMMAND="cd ~/Projetos && nvim"
SHELL_RC="$HOME/.bashrc"

# Detecta se está usando zsh
if [ -n "$ZSH_VERSION" ]; then
  SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
  SHELL_RC="$HOME/.bashrc"
elif [ -f "$HOME/.zshrc" ]; then
  SHELL_RC="$HOME/.zshrc"
fi

# Adiciona o alias se ainda não existir
if ! grep -Fxq "alias $ALIAS_NAME=\"$ALIAS_COMMAND\"" "$SHELL_RC"; then
  echo "alias $ALIAS_NAME=\"$ALIAS_COMMAND\"" >>"$SHELL_RC"
  echo "[OK] Alias '$ALIAS_NAME' adicionado a $SHELL_RC"
else
  echo "[INFO] Alias '$ALIAS_NAME' já existe em $SHELL_RC"
fi
