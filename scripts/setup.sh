set -e

echo "🌹 Rose Symptom Checker - Setup Script"
echo "========================================"

# Check if Python 3.11+ is installed
echo "Checking Python version..."
python3 --version

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "✓ uv is already installed"
fi

# Create virtual environment
echo "Creating virtual environment..."
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
uv pip install -e ".[dev]"

# Create necessary directories
echo "Creating project directories..."
mkdir -p src/ml data/raw data/processed tests

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configurations"
fi

# Generate secret key
if command -v openssl &> /dev/null; then
    SECRET_KEY=$(openssl rand -hex 32)
    echo "Generated SECRET_KEY: $SECRET_KEY"
    echo "Please update SECRET_KEY in .env file"
fi

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your configurations"
echo "2. Run: source .venv/bin/activate"
echo "3. Train ML model: python scripts/train_model.py"
echo "4. Start with Docker: docker-compose up --build"
echo "   OR start locally: uvicorn src.main:app --reload"