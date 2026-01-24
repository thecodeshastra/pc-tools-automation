install_docker() {
  if command -v docker >/dev/null 2>&1; then
    echo "Docker already installed"
    return 0
  fi

  echo "Installing Docker (latest)..."

  sudo apt-get update
  sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

  # Create keyrings directory
  sudo mkdir -p /etc/apt/keyrings

  # Download Docker GPG key (new recommended way)
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    -o /etc/apt/keyrings/docker.asc

  sudo chmod a+r /etc/apt/keyrings/docker.asc

  # Add Docker repository (Ubuntu 24.04 - noble)
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu noble stable" \
    | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  sudo apt-get update

  sudo apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin

  sudo systemctl enable docker
  sudo systemctl start docker

  echo "Docker installed successfully"
}

setup_docker_permissions() {
  sudo usermod -aG docker $USER
  echo "Added $USER to docker group. Log out & back in to apply changes."
}
