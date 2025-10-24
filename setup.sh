#!/bin/bash

# IntellAgent Web Interface Setup Script
echo "🚀 IntellAgent Web Interface Setup"
echo "=================================="

# Check if Python 3.9+ is available
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
major_version=$(echo $python_version | cut -d. -f1)
minor_version=$(echo $python_version | cut -d. -f2)

if [[ $major_version -lt 3 ]] || [[ $major_version -eq 3 && $minor_version -lt 9 ]]; then
    echo "❌ Python 3.9+ required. Found Python $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "🔧 Running health check..."
python health_check.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure API keys: source venv/bin/activate && python setup_api_keys.py"
echo "2. Launch web interface: source venv/bin/activate && python launch_web_interface.py"
echo ""
echo "Or use the quick start:"
echo "   source venv/bin/activate"
echo "   python setup_api_keys.py"
echo "   python launch_web_interface.py"