#!/usr/bin/env bash

set -euo pipefail

# read config file
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$ROOT_DIR")"

# read other module files
# development tools
source "$ROOT_DIR/tools/ulla.sh"
source "$ROOT_DIR/config.sh"
source "$ROOT_DIR/tools/uv.sh"
source "$ROOT_DIR/tools/nvm_npm.sh"
source "$ROOT_DIR/tools/postgresql.sh"
source "$ROOT_DIR/tools/docker.sh"
source "$ROOT_DIR/tools/antigravity.sh"
source "$ROOT_DIR/tools/vscode.sh"
source "$ROOT_DIR/tools/ollama.sh"

# office tools and packages
source "$ROOT_DIR/tools/pcoip_client.sh"
install_pcoip_client

log "Starting workstation bootstrap"

# running the install base function
install_base_packages
install_ulla
# IDE
install_antigravity
install_vscode
# development tools
install_uv
install_nvm
install_node
install_postgresql
install_docker
setup_docker_permissions
# AI tools
install_ollama

# restore home folder
source "$ROOT_DIR/restore_home.sh"
restore_home_folder
fix_permissions
