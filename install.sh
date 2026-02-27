#!/bin/bash
# One-line installer for jules CLI
# Usage: curl -sSL https://raw.githubusercontent.com/yourusername/jules-cli/main/install.sh | bash
# Or from cloned repo: ./install.sh --local

set -e

LOCAL_INSTALL=false
if [[ "$1" == "--local" ]]; then
    LOCAL_INSTALL=true
fi

INSTALL_DIR="${JULES_CLI_DIR:-$HOME/.jules-cli}"
REPO_URL="https://github.com/yourusername/jules-cli.git"
REPO_DIR="$INSTALL_DIR/jules-cli"
BIN_DIR="$HOME/.local/bin"

echo "🚀 Installing jules CLI..."

# Create install directory
mkdir -p "$INSTALL_DIR"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Clone or update repository (unless --local is specified)
if [ "$LOCAL_INSTALL" = true ]; then
    echo "📥 Installing from current directory..."
    REPO_DIR="$(pwd)"
    cd "$REPO_DIR"
elif [ -d "$REPO_DIR" ]; then
    echo "📥 Updating existing installation..."
    cd "$REPO_DIR"
    git pull
else
    echo "📥 Cloning repository..."
    git clone "$REPO_URL" "$REPO_DIR"
    cd "$REPO_DIR"
fi

# Create virtual environment and install
echo "🔧 Setting up virtual environment..."
if [ ! -d ".venv" ]; then
    uv venv .venv --python 3.11
fi
uv pip install -e .

# Create bin directory
mkdir -p "$BIN_DIR"

# Create wrapper script (escape $ for literals, expand $REPO_DIR)
cat > "$BIN_DIR/jules" << EOF
#!/bin/bash
# Wrapper script for jules CLI using uv venv

PROJECT_DIR="$REPO_DIR"
JULES_EXEC="\$PROJECT_DIR/.venv/bin/jules"

if [ -f "\$JULES_EXEC" ]; then
    exec "\$JULES_EXEC" "\$@"
else
    echo "Error: jules not found in .venv at \$JULES_EXEC" >&2
    echo "Run: cd \$PROJECT_DIR && uv pip install -e ." >&2
    exit 1
fi
EOF

chmod +x "$BIN_DIR/jules"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "⚠️  $HOME/.local/bin is not in your PATH"
    echo "   Add this to your ~/.zshrc or ~/.bashrc:"
    echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "   Run: jules --help"
echo "   Or:  $HOME/.local/bin/jules --help"
echo ""
echo "   To configure: jules config init"
echo ""
