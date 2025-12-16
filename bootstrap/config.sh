#!/usr/bin/env bash

HOME_FOLDER="$ROOT_DIR/home"

APT_PACKAGES=(
  curl
  rsync
  rar
  git-all
  build-essential
  python3-dev
  python3-venv
  python3-pip
)

log() {
  echo -e "\n\033[1;32m[+] $1\033[0m"
}

warn() {
  echo -e "\033[s1;33m[!] $1\033[0m"
}

error() {
  echo -e "\033[1;31m[✗] $1\033[0m"
  exit 1
}

require_sudo() {
  if [[ "$EUID" -eq 0 ]]; then
    error "Do not run as root"
  fi
  sudo -v
}

detect_distro() {
  if [[ -f /etc/debian_version ]]; then
    DISTRO="debian"
  else
    error "Unsupported distro"
  fi
}
