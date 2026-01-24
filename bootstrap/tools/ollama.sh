install_ollama() {
  echo "📦 Installing Ollama..."

  if command -v ollama >/dev/null 2>&1; then
    echo "✅ Ollama is already installed"
    return 0
  fi

  curl -fsSL https://ollama.com/install.sh | sh

  if command -v ollama >/dev/null 2>&1; then
    echo "🎉 Ollama installed successfully"
  else
    echo "❌ Ollama installation failed"
    return 1
  fi
}
