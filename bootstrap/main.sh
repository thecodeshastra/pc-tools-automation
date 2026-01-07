#!/usr/bin/env bash

set -euo pipefail

# read config file
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# read other module files
source "$ROOT_DIR/config.sh"

log "Starting workstation bootstrap"

# Install base system packages
source "$ROOT_DIR/install/base.sh"
# running the install base function
install_base_packages
install_uv

# sourcing additional packages
source "$ROOT_DIR/install/antigravity.sh"
source "$ROOT_DIR/install/pcoip.sh"
# installing additional packages
install_antigravity
install_pcoip_client

# restore home folder
source "$ROOT_DIR/restore_home.sh"
restore_home_folder

# Update permissions
fix_permissions() {
  log "Fixing permissions"
  chmod 700 "$HOME/.ssh" 2>/dev/null || true
  chmod 600 "$HOME/.ssh/"* 2>/dev/null || true
  sudo chown -R "$USER:$USER" "$HOME"
}
fix_permissions