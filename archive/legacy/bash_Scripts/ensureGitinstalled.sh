#!/bin/bash

if ! command -v git &>/dev/null; then
	echo "[INFO] Git nao encontrado. Instalando Git..."
	sudo apt update
	sudo apt install -y git
	echo "[OK] Git instalado com sucesso."
else
	echo "[OK] Git ja esta instalado."
fi
