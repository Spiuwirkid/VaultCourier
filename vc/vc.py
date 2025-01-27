import os
import sys
import requests
import shutil
from datetime import datetime

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("\033[91m[ERROR]\033[0m TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing. Please set it in your environment variables.")
    sys.exit(1)

INFO_COLOR = "\033[94m"    
SUCCESS_COLOR = "\033[92m" 
ERROR_COLOR = "\033[91m"   
RESET_COLOR = "\033[0m"   

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        print(f"{INFO_COLOR}[INFO]{RESET_COLOR} Message sent to Telegram: '{message}'")
    except requests.exceptions.RequestException as e:
        print(f"{ERROR_COLOR}[ERROR]{RESET_COLOR} Failed to send message to Telegram: {e}")
        return False
    return True

def send_file_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    try:
        file_name = os.path.basename(file_path)
        message = f"Here is the file you requested:\n\n<code>{file_name}</code>"
        
        if send_telegram_message(message):
            print(f"{INFO_COLOR}[INFO]{RESET_COLOR} Message sent to Telegram: 'Here is the file you requested: {file_name}'")

        with open(file_path, "rb") as file:
            files = {"document": file}
            payload = {"chat_id": CHAT_ID}
            response = requests.post(url, data=payload, files=files, timeout=60)
            response.raise_for_status()

        print(f"{SUCCESS_COLOR}[SUCCESS]{RESET_COLOR} File '{file_name}' has been successfully sent to Telegram.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"{ERROR_COLOR}[ERROR]{RESET_COLOR} Failed to send file to Telegram: {e}")
    except FileNotFoundError:
        print(f"{ERROR_COLOR}[ERROR]{RESET_COLOR} File '{file_path}' does not exist.")
    return False


def zip_folder(folder_path):
    try:
        folder_name = os.path.basename(os.path.normpath(folder_path))  # Get folder name
        zip_name = f"{folder_name}.zip"  # Create zip name based on folder name
        shutil.make_archive(folder_name, "zip", folder_path)
        zip_path = f"{folder_name}.zip"  # Path to the generated zip file
        print(f"{INFO_COLOR}[INFO]{RESET_COLOR} Folder '{folder_path}' has been zipped into '{zip_path}'.")
        return zip_path
    except Exception as e:
        print(f"{ERROR_COLOR}[ERROR]{RESET_COLOR} Failed to zip folder: {e}")
        return None

def main():
    if len(sys.argv) < 3:
        print(f"""
{INFO_COLOR}Usage:{RESET_COLOR}
  vc -f <file_path> 
  vc -d <folder_path> 
""")
        sys.exit(1)

    option = sys.argv[1]
    path = sys.argv[2]

    if option == "-f":
        # Send file
        if os.path.isfile(path):
            if not send_file_to_telegram(path):
                print(f"{ERROR_COLOR}[ERROR]{RESET_COLOR} Failed to send file.")
        else:
            print(f"{ERROR_COLOR}[ERROR]{RESET_COLOR} File '{path}' does not exist.")
    elif option == "-d":
        # Send folder (auto-zip)
        if os.path.isdir(path):
            zip_path = zip_folder(path)
            if zip_path and send_file_to_telegram(zip_path):
                print(f"{SUCCESS_COLOR}[SUCCESS]{RESET_COLOR} Folder '{path}' has been successfully sent to Telegram.")
            else:
                print(f"{ERROR_COLOR}[ERROR]{RESET_COLOR} Failed to send folder.")
        else:
            print(f"{ERROR_COLOR}[ERROR]{RESET_COLOR} Folder '{path}' does not exist.")
    else:
        print(f"{ERROR_COLOR}[ERROR]{RESET_COLOR} Invalid option. Use -f for file or -d for folder.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        print(f"{INFO_COLOR}[INFO]{RESET_COLOR} VaultCourier is starting...")
        main()
        print(f"{SUCCESS_COLOR}[SUCCESS]{RESET_COLOR} VaultCourier finished its operation.")
    except KeyboardInterrupt:
        print(f"\n{ERROR_COLOR}[CANCELLED]{RESET_COLOR} Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"{ERROR_COLOR}[ERROR]{RESET_COLOR} An error occurred: {e}")
