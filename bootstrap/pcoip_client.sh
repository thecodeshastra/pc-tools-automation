install_pcoip_client() {
  log "Installing PCoIP Client"

  if dpkg -l | grep -q pcoip-client; then
    log "PCoIP Client already installed"
    return
  fi

  curl -1sLf https://dl.anyware.hp.com/DeAdBCiUYInHcSTy/pcoip-client/cfg/setup/bash.deb.sh \
    | sudo -E distro=ubuntu codename=noble bash

  sudo apt update -y
  sudo apt install -y pcoip-client
}
