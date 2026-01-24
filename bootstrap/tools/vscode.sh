install_vscode() {
  if command -v code >/dev/null 2>&1; then
    echo "VS Code already installed"
    return 0
  fi

  echo "Installing VS Code (latest)..."

  sudo apt-get update
  sudo apt-get install -y \
    wget \
    gpg \
    apt-transport-https

  wget -qO- https://packages.microsoft.com/keys/microsoft.asc \
    | gpg --dearmor \
    | sudo tee /etc/apt/keyrings/packages.microsoft.gpg > /dev/null

  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/packages.microsoft.gpg] \
    https://packages.microsoft.com/repos/code stable main" \
    | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null

  sudo apt-get update
  sudo apt-get install -y code

  echo "VS Code installed successfully"
}
