install_base_packages() {
  log "Installing base system packages"
  sudo apt update -y
  sudo apt upgrade -y
  sudo apt install -y "${APT_PACKAGES[@]}"
}


install_uv() {
  log "Installing Astral uv"

  if command -v uv &>/dev/null; then
    log "uv already installed"
    return
  fi

  curl -LsSf https://astral.sh/uv/install.sh | sh
}
