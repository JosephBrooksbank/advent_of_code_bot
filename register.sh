#!/bin/bash

SERVICE_NAME="advent_of_code_bot"
WORKING_DIR=$(pwd)
PYTHON_ENV="$WORKING_DIR/venv/bin/python"
MAIN_SCRIPT="$WORKING_DIR/main.py"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

# Check for virtual environment
if [ ! -f "$PYTHON_ENV" ]; then
  echo "Virtual environment not found. Please set up a virtual environment in the current directory (venv)."
  exit 1
fi

# Check for main.py
if [ ! -f "$MAIN_SCRIPT" ]; then
  echo "main.py not found in the current directory."
  exit 1
fi

# Create the systemd service file
echo "Creating systemd service file at $SERVICE_FILE..."

sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Python Application Service ($SERVICE_NAME)
After=network.target

[Service]
Type=simple
WorkingDirectory=$WORKING_DIR
ExecStart=$PYTHON_ENV $MAIN_SCRIPT
Restart=on-failure
User=$(whoami)
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd and enable the service
echo "Reloading systemd and enabling $SERVICE_NAME..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME

echo "Service $SERVICE_NAME registered successfully."
echo "You can start it using: sudo systemctl start $SERVICE_NAME"
echo "Check logs using: sudo journalctl -u $SERVICE_NAME -f"
