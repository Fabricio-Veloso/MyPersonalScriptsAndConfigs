# Instala neovim no wsl
function install-NeovimWSL {
  Install-WSL-Dependencies

  echo 'Instalando Neovim'
  # Adicionar repositório oficial do Neovim
  sudo apt install -y software-properties-common
  sudo add-apt-repository ppa:neovim-ppa/unstable -y
  sudo apt update
  sudo apt install -y neovim

  echo 'Instalando Luarocks...'
  sudo apt install -y luarocks

  echo 'Preparando estrutura do Neovim...'
  mkdir -p ~/.config
  rm -rf ~/.config/nvim

  echo 'Verificando repositório de configuração do usuário Fabricio...'

  # Verifica se o repositório já existe
  if [ -d "~/.config/nvim/.git" ]; then
  echo 'Repositório encontrado! Atualizando com git pull...'
  cd ~/.config/nvim && git pull
  else
  echo 'Repositório não encontrado! Clonando configuração...'
  git clone --depth 1 https://github.com/Fabricio-Veloso/nvim.git ~/.config/nvim
  fi

  echo 'Setup finalizado! Agora é só abrir o nvim :)'
}

