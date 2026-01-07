install_rar() {
  log "Installing RAR manually"

  if command -v rar &>/dev/null; then
    log "RAR already installed"
    return
  fi

  TMP_DIR="$(mktemp -d)"
  pushd "$TMP_DIR" >/dev/null

  curl -O https://www.rarlab.com/rar/rarlinux-x64-621.tar.gz
  tar -xzf rarlinux-x64-621.tar.gz

  cd rar

  sudo cp rar unrar /usr/local/bin/
  sudo chmod +x /usr/local/bin/rar /usr/local/bin/unrar

  popd >/dev/null
  rm -rf "$TMP_DIR"

  log "RAR installed successfully"
}

install_rar
