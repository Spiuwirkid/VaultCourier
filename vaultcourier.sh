#!/bin/bash

# VaultCourier Installation Script

echo -e "\033[94m[INFO]\033[0m Starting VaultCourier installation..."
sleep 1

# Check Python installation
echo -e "\033[94m[INFO]\033[0m Checking Python installation..."
sleep 1
if ! command -v python3 &> /dev/null
then
    echo -e "\033[91m[ERROR]\033[0m Python 3 is not installed. Please install it first."
    exit 1
fi

# Check pip installation
echo -e "\033[94m[INFO]\033[0m Checking pip installation..."
sleep 1
if ! command -v pip &> /dev/null
then
    read -p "pip is not installed. Do you want to install it? (y/n): " install_pip
    if [[ "$install_pip" == "y" || "$install_pip" == "Y" ]]; then
        if [ -f /etc/debian_version ]; then
            echo -e "\033[94m[INFO]\033[0m Installing pip using apt..."
            sleep 1
            sudo apt update && sudo apt install python3-pip -y
        elif [ -f /etc/redhat-release ]; then
            echo -e "\033[94m[INFO]\033[0m Installing pip using yum..."
            sleep 1
            sudo yum install python3-pip -y
        else
            echo -e "\033[91m[ERROR]\033[0m Unsupported OS. Please install pip manually."
            exit 1
        fi
    else
        echo -e "\033[91m[ERROR]\033[0m pip installation skipped. Exiting installation."
        exit 1
    fi
fi

# Install Python dependencies
echo -e "\033[94m[INFO]\033[0m Installing Python dependencies..."
sleep 1
if pip install -r vc/requirements.txt 2>&1 | grep -q "externally-managed-environment"; then
    echo -e "\033[91m[ERROR]\033[0m pip is restricted in this environment. Using apt to install dependencies..."
    sleep 1
    while IFS= read -r package; do
        package_name=$(echo "$package" | cut -d= -f1)  # Ambil hanya nama paket tanpa versi
        sudo apt install -y "python3-$package_name"
    done < vc/requirements.txt
fi

# Configure environment variables
echo -e "\033[94m[INFO]\033[0m Configuring environment variables..."
sleep 1
read -p "Enter your Telegram Bot Token: " bot_token
read -p "Enter your Telegram Chat ID: " chat_id

if [ -n "$ZSH_VERSION" ]; then
  PROFILE_FILE=~/.zshrc
elif [ -n "$BASH_VERSION" ]; then
  PROFILE_FILE=~/.bashrc
else
  echo -e "\033[91m[ERROR]\033[0m Unable to detect shell. Please set the environment variables manually."
  exit 1
fi

echo "export TELEGRAM_BOT_TOKEN=\"$bot_token\"" >> $PROFILE_FILE
echo "export TELEGRAM_CHAT_ID=\"$chat_id\"" >> $PROFILE_FILE
echo -e "\033[92m[SUCCESS]\033[0m Environment variables added to $PROFILE_FILE."
sleep 1

# Create alias for 'vc'
echo -e "\033[94m[INFO]\033[0m Creating alias for 'vc'..."
sleep 1
unalias vc 2>/dev/null  # Hapus alias lama jika ada
echo "alias vc='python3 $(pwd)/vc/vc.py'" >> $PROFILE_FILE
echo -e "\033[92m[SUCCESS]\033[0m Alias 'vc' created."
sleep 1

# Completion message
echo -e "\033[92m[SUCCESS]\033[0m VaultCourier installation complete!"
echo -e "\033[94m[INFO]\033[0m Usage examples:"
echo -e "  vc -f <file_path>   : Send a file to Telegram."
echo -e "  vc -d <folder_path> : Send a folder to Telegram (auto-zipped)."
echo -e "  vc --help           : Show this help message."

# Provide manual instruction for source command
echo -e "\033[91m[IMPORTANT]\033[0m \033[1;33mTo activate the 'vc' command, you MUST manually run:\033[0m"
echo -e "\033[1;32m  source $PROFILE_FILE\033[0m"
echo -e "\033[1;33mMake sure to execute this command before using 'vc'.\033[0m"
echo -e "\033[1;31mIf you skip this step, the 'vc' command will not work.\033[0m"

