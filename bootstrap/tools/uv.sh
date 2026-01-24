install_uv() {
  log "Installing Astral uv"

  if command -v uv &>/dev/null; then
    log "uv already installed"
    return
  fi

  curl -LsSf https://astral.sh/uv/install.sh | sh
}
