import os
import sys
import shutil
import logging
import argparse
from pathlib import Path
from typing import Optional
import requests
from tqdm import tqdm
from tenacity import retry, stop_after_attempt, wait_exponential, before_log
from dotenv import load_dotenv
from colorama import init, Fore
import zipfile

init(autoreset=True)
logging.basicConfig(
    level=logging.INFO,
    format=f"{Fore.CYAN}%(asctime)s{Fore.RESET} [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("vaultcourier.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB Telegram limit
BOT_TOKEN_REGEX = r"^\d+:[a-zA-Z0-9_-]{35}$"  # Token validation regex

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    logger.error("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured in .env")
    sys.exit(1)

if not (BOT_TOKEN and len(BOT_TOKEN.split(":")) == 2):
    logger.error("Invalid TELEGRAM_BOT_TOKEN format")
    sys.exit(1)

class TelegramClient:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{BOT_TOKEN}"
        self.session = requests.Session()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), before=before_log(logger, logging.DEBUG))
    def send_message(self, message: str) -> bool:
        """Send a message to the configured chat."""
        url = f"{self.base_url}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
        try:
            response = self.session.post(url, json=payload, timeout=15)
            response.raise_for_status()
            logger.info(f"Message sent to Telegram: '{message[:50]}...'")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to send message: {e}")
            return False

    def send_file(self, file_path: Path, message: Optional[str] = None) -> bool:
        """Send a file to the Telegram chat."""
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            self.report_error(f"File not found: {file_path}")
            return False

        logger.info(f"File '{file_path.name}' is being sent to Telegram...")
        if file_path.stat().st_size > MAX_FILE_SIZE:
            logger.error(f"File size exceeds limit: {self._human_size(file_path.stat().st_size)} > 50MB")
            self.report_error(f"File size exceeds limit: {self._human_size(file_path.stat().st_size)} > 50MB")
            return False

        preview_msg = message or f"📁 File: {file_path.name}"
        if not self.send_message(f"{preview_msg}\n\n<code>Size: {self._human_size(file_path.stat().st_size)}</code>"):
            logger.error("Failed to send preview message. Aborting file upload.")
            return False

        try:
            with file_path.open('rb') as f:
                url = f"{self.base_url}/sendDocument"
                files = {"document": (file_path.name, f)}
                data = {"chat_id": CHAT_ID}

                with tqdm(total=file_path.stat().st_size, unit="B", unit_scale=True, desc=f"Uploading {file_path.name}") as pbar:
                    response = self.session.post(url, files=files, data=data, timeout=60)
                    response.raise_for_status()
                    pbar.update(file_path.stat().st_size)

            logger.info(f"Successfully sent file: {file_path.name}")
            logger.info(f"Successfully sent: {file_path.name}")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to upload file: {e}")
            self.report_error(f"Failed to upload file: {file_path.name} - {e}")
            return False

    def report_error(self, error_message: str):
        """Report errors to Telegram chat."""
        error_msg = f"⚠️ <b>Error:</b> {error_message}"
        self.send_message(error_msg)

    @staticmethod
    def _human_size(size: int) -> str:
        """Convert file size to human-readable format."""
        units = ['B', 'KB', 'MB', 'GB']
        index = 0
        while size >= 1024 and index < len(units) - 1:
            size /= 1024
            index += 1
        return f"{size:.2f} {units[index]}"

def zip_folder(folder_path: Path) -> Optional[Path]:
    """Compress folder with progress tracking."""
    if not folder_path.exists() or not folder_path.is_dir():
        logger.error(f"Folder not found or invalid: {folder_path}")
        client.report_error(f"Folder not found or invalid: {folder_path}")
        return None

    try:
        logger.info(f"VaultCourier is starting...")
        zip_path = folder_path.with_suffix('.zip')
        total_size = sum(f.stat().st_size for f in folder_path.rglob('*') if f.is_file())

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf, tqdm(
            total=total_size, unit="B", unit_scale=True, desc=f"Zipping {folder_path.name}"
        ) as pbar:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(folder_path.parent)
                    zipf.write(file_path, arcname)
                    pbar.update(file_path.stat().st_size)

        logger.info(f"Folder '{folder_path}' has been zipped into '{zip_path.name}'.")
        return zip_path
    except Exception as e:
        logger.error(f"Failed to zip folder: {e}")
        client.report_error(f"Failed to zip folder: {folder_path.name} - {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description="VaultCourier - Secure File Transfer via Telegram",
        epilog="Example: python vc.py --file example1.txt example2.jpg --message 'Here are the files'"
    )
    parser.add_argument("-f", "--file", nargs="+", help="File(s) to send (support multiple files)")
    parser.add_argument("-d", "--directory", help="Directory to compress and send")
    parser.add_argument("-m", "--message", help="Custom message for file upload")

    args = parser.parse_args()
    client = TelegramClient()

    try:
        if args.file:
            for file_path in args.file:
                path = Path(file_path)
                if not path.exists():
                    logger.error(f"File not found: {path}")
                    client.report_error(f"File not found: {path}")
                elif client.send_file(path, args.message):
                    logger.info(f"Successfully sent: {path.name}")
        elif args.directory:
            dir_path = Path(args.directory)
            if not dir_path.exists():
                logger.error(f"Folder not found: {dir_path}")
                client.report_error(f"Folder not found: {dir_path}")
            else:
                zip_path = zip_folder(dir_path)
                if zip_path and client.send_file(zip_path, args.message):
                    logger.info(f"Successfully sent directory as ZIP: {zip_path.name}")
                    zip_path.unlink() 
                    logger.info(f"VaultCourier finished its operation.")
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        client.report_error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()