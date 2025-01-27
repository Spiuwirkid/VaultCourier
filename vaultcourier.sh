#!/bin/bash

# VaultCourier Installer

echo -e "\033[94m[INFO]\033[0m Starting VaultCourier installation..."

# Step 1: Install dependencies
echo -e "\033[94m[INFO]\033[0m Installing Python dependencies..."
pip install -r vc/requirements.txt

# Step 2: Set environment variables
echo -e "\033[94m[INFO]\033[0m Configuring environment variables..."
read -p "Enter your Telegram Bot Token: " bot_token
read -p "Enter your Telegram Chat ID: " chat_id

# Save environment variables to ~/.bashrc or ~/.zshrc
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

# Step 3: Create alias for vc
echo -e "\033[94m[INFO]\033[0m Creating alias for 'vc'..."
echo "alias vc='python3 $(pwd)/vc/vaultcourier.py'" >> $PROFILE_FILE
echo -e "\033[92m[SUCCESS]\033[0m Alias 'vc' created. Restart your terminal or run 'source $PROFILE_FILE' to apply changes."

# Step 4: Finish
echo -e "\033[92m[SUCCESS]\033[0m VaultCourier installation complete!"
echo -e "\033[94m[INFO]\033[0m Usage examples:"
echo -e "  vc -f <file_path>    # Send a file"
echo -e "  vc -d <folder_path>  # Send a folder (auto-zipped)"
