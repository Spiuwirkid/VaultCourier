#!/bin/bash

# VaultCourier Installation Script

echo -e "\033[94m[INFO]\033[0m Starting VaultCourier installation..."
sleep 1

echo -e "\033[94m[INFO]\033[0m Checking Python installation..."
sleep 1
if ! command -v python3 &> /dev/null
then
    echo -e "\033[91m[ERROR]\033[0m Python 3 is not installed. Please install it first."
    exit 1
fi

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

echo -e "\033[94m[INFO]\033[0m Installing Python dependencies..."
sleep 1
pip install -r vc/requirements.txt

echo -e "\033[94m[INFO]\033[0m Configuring environment variables using .env file..."
sleep 1
if [ ! -f .env ]; then
    read -p "Enter your Telegram Bot Token: " bot_token
    read -p "Enter your Telegram Chat ID: " chat_id

    echo "TELEGRAM_BOT_TOKEN=$bot_token" > .env
    echo "TELEGRAM_CHAT_ID=$chat_id" >> .env
    echo -e "\033[92m[SUCCESS]\033[0m .env file created successfully."
else
    echo -e "\033[93m[WARNING]\033[0m .env file already exists. Please update it manually if needed."
fi

echo -e "\033[94m[INFO]\033[0m Creating alias for 'vc'..."
sleep 1
PROFILE_FILE=""
if [ -n "$ZSH_VERSION" ]; then
  PROFILE_FILE=~/.zshrc
elif [ -n "$BASH_VERSION" ]; then
  PROFILE_FILE=~/.bashrc
else
  echo -e "\033[91m[ERROR]\033[0m Unable to detect shell. Please set the alias manually."
  exit 1
fi

unalias vc 2>/dev/null  
echo "alias vc='python3 $(pwd)/vc/vc.py'" >> $PROFILE_FILE
echo -e "\033[92m[SUCCESS]\033[0m Alias 'vc' created in $PROFILE_FILE."

echo -e "\033[92m[SUCCESS]\033[0m VaultCourier installation complete!"
echo -e "\033[94m[INFO]\033[0m Usage examples:"
echo -e "  vc -f <file_path>   : Send a file to Telegram."
echo -e "  vc -d <folder_path> : Send a folder to Telegram (auto-zipped)."
echo -e "  vc --help           : Show this help message."

echo -e "\033[91m[IMPORTANT]\033[0m \033[1;33mTo activate the 'vc' command, you MUST manually run:\033[0m"
echo -e "\033[1;32m  source $PROFILE_FILE\033[0m"
echo -e "\033[1;33mMake sure to execute this command before using 'vc'.\033[0m"
echo -e "\033[1;31mIf you skip this step, the 'vc' command will not work.\033[0m"
