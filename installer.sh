#!/bin/bash

# Function to check the last command status
check_status() {
  if [ $? -ne 0 ]; then
    echo "Error occurred. Exiting."
    exit 1
  fi
}

# Update and install dependencies
echo "Updating system packages and installing dependencies..."
sudo apt update && sudo apt upgrade -y
check_status

sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git
check_status

# Install pyenv
echo "Installing pyenv..."
curl https://pyenv.run | bash
check_status

# Add pyenv to the bash profile
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# Source the bash profile to load pyenv
source ~/.bashrc

# Install Python 3.10.0 using pyenv
echo "Installing Python 3.10.0..."
pyenv install 3.10.0
check_status

# Create a virtual environment named 'yt_download'
echo "Creating virtual environment 'yt_download' with Python 3.10.0..."
pyenv virtualenv 3.10.0 yt_download
check_status

# Activate the virtual environment
echo "Activating virtual environment 'yt_download'..."
pyenv activate yt_download
check_status

# Update pip to the latest version
echo "Updating pip..."
pip install --upgrade pip
check_status

# Install yt-dlp
echo "Installing yt-dlp..."
pip install yt-dlp
check_status

# Clone the repository into the home directory
echo "Cloning the repository into the home directory..."
cd ~
git clone https://github.com/www.github.com
check_status

# Add function to .bashrc
echo "Adding 'yd' function to .bashrc..."
cat << 'EOF' >> ~/.bashrc

function yd {
    # Activate pyenv environment
    pyenv activate yt_download

    clear
    # Run the Python script
    cd ~/youtube_downloader
    python yd.py

    # Check if python script execution was successful
    if [ $? -ne 0 ]; then
        echo "Failed to run yd.py"
        return 1
    fi

    echo "Script executed successfully"
}
EOF

# Source .bashrc to apply changes
echo "Sourcing .bashrc to apply changes..."
source ~/.bashrc

echo "Setup complete. The function 'yd' has been added to your .bashrc, you can start the program typing yd in your terminal."
