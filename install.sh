#!/bin/bash

INSTALL_DIR="$HOME/.c0admin"
EXECUTABLE_NAME="c0admin"
LAUNCHER_PATH="/usr/local/bin/$EXECUTABLE_NAME"
REPO_URL="https://github.com/mbrell/c0admin.git"
echo "c0admin installation starting..."

if [ -d "$INSTALL_DIR" ]; then
   echo "Previous installation found. Removing..."
   rm -rf "$INSTALL_DIR"
fi

echo "Downloading GitHub repository..."
git clone "$REPO_URL" "$INSTALL_DIR"

echo "Creating Python virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"
source "$INSTALL_DIR/venv/bin/activate"

if [ -f "$INSTALL_DIR/requirements.txt" ]; then
   echo "Installing packages..."
   pip install -r "$INSTALL_DIR/requirements.txt"
else
   echo "requirements.txt not found. Installing 'colorama', 'pyperclip', 'google-generativeai' with pip..."
   pip install colorama pyperclip google-generativeai requests
fi
deactivate
# create script
echo "Setting up $EXECUTABLE_NAME command..."
sudo bash -c "cat > $LAUNCHER_PATH" << EOF
#!/bin/bash
source "$INSTALL_DIR/venv/bin/activate"
python3 "$INSTALL_DIR/main.py"
EOF
sudo chmod +x "$LAUNCHER_PATH"
echo "Installation completed!"
echo "You can run the application by typing 'c0admin' in terminal."
