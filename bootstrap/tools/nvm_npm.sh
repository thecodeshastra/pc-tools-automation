install_nvm() {
  local NVM_VERSION="v0.39.7"

  if command -v nvm >/dev/null 2>&1; then
    echo "nvm already installed"
    return 0
  fi

  echo "Installing nvm $NVM_VERSION..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/$NVM_VERSION/install.sh | bash

  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

  echo "nvm $NVM_VERSION installation complete"
}


install_node() {
  local NODE_VERSION="lts/*"

  if ! command -v nvm >/dev/null 2>&1; then
    echo "nvm is not installed. Please install nvm first."
    return 1
  fi

  echo "Installing Node.js $NODE_VERSION..."
  nvm install $NODE_VERSION
  nvm use $NODE_VERSION
  nvm alias default $NODE_VERSION

  echo "Node.js $NODE_VERSION installation complete"
}
