#!/usr/bin/env bash
set -e

echo "Installing pdf2video..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found. Install it first:"
    echo "  sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

# Install system deps
if command -v apt &> /dev/null; then
    echo "Installing system dependencies..."
    sudo apt-get update -qq
    sudo apt-get install -y -qq ffmpeg tesseract-ocr tesseract-ocr-fra tesseract-ocr-eng >/dev/null 2>&1
elif command -v brew &> /dev/null; then
    brew install ffmpeg tesseract tesseract-lang 2>/dev/null
else
    echo "Warning: could not install system deps automatically."
    echo "Make sure ffmpeg and tesseract-ocr are installed."
fi

# Install pdf2video
pip3 install --user pdf2video

# Add to PATH if needed
LOCAL_BIN="$HOME/.local/bin"
if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$HOME/.bashrc"
    export PATH="$LOCAL_BIN:$PATH"
fi

echo ""
echo "Done! Usage:"
echo "  pdf2video /path/to/course.pdf"
echo "  pdf2video /path/to/course.pdf -o output.mp4"
echo "  pdf2video /path/to/course.pdf --quality qh"
