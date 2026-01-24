install_postgresql() {
  if command -v psql >/dev/null 2>&1; then
    echo "PostgreSQL already installed"
    return 0
  fi

  echo "Installing PostgreSQL (latest)..."

  sudo apt-get update
  sudo apt-get install -y curl ca-certificates gnupg

  curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc \
    | sudo gpg --dearmor -o /etc/apt/keyrings/postgresql.gpg

  echo \
    "deb [signed-by=/etc/apt/keyrings/postgresql.gpg] \
    http://apt.postgresql.org/pub/repos/apt \
    $(lsb_release -cs)-pgdg main" \
    | sudo tee /etc/apt/sources.list.d/pgdg.list > /dev/null

  sudo apt-get update
  sudo apt-get install -y postgresql postgresql-contrib

  sudo systemctl enable postgresql
  sudo systemctl start postgresql

  echo "PostgreSQL installed successfully"
  psql --version
}
