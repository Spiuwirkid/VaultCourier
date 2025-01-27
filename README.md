# VaultCourier 🚀

Welcome to **VaultCourier**, your ultimate solution for securely sending files and folders directly to Telegram with just a few commands. Simple, powerful, and ready to use. 🔐📤

---

## **Features** ✨
- **Send Files:** Transfer any file to Telegram easily.
- **Send Folders:** Automatically compress folders into `.zip` and send them seamlessly.
- **User-Friendly:** Minimal setup with one command installation.
- **Customizable:** Easily configure Telegram Bot Token and Chat ID.
- **Lightweight:** Designed for performance and simplicity.

---

## **Requirements** 🔧
Before installing VaultCourier, ensure you have the following installed:

1. **Python 3.x**
   - Check if Python is installed:
     ```bash
     python3 --version
     ```
   - If not installed, download and install it from [python.org](https://www.python.org/downloads/).

2. **pip** (Python package manager)
   - Check if pip is installed:
     ```bash
     pip --version
     ```
   - If not installed, install it with:
     ```bash
     sudo apt update && sudo apt install python3-pip -y  # For Debian/Ubuntu
     sudo yum install python3-pip -y                    # For CentOS/RedHat
     ```

---

## **How to Create a Telegram Bot and Get Chat ID** 🔧

### **Step 1: Create a Telegram Bot**
1. Open Telegram and search for **@BotFather**.
2. Start a chat with BotFather and send the command:
   ```
   /newbot
   ```
3. Follow the instructions to:
   - Give your bot a name (e.g., `VaultCourierBot`).
   - Create a unique username for the bot (e.g., `VaultCourier_Bot`).
4. Once done, BotFather will provide you with a **Bot Token**. Save this token; you will need it later.

   **Example:**
   ```
   123456:ABCdefGHIjklMNOpqrSTUvwxYZ
   ```

![Create Bot with BotFather](https://i.ibb.co.com/hmk1m1d/Screenshot-2025-01-27-135539.png)

---

### **Step 2: Get Your Chat ID**
1. Search for **@userinfobot** on Telegram and start a chat.
2. Send the command:
   ```
   /start
   ```
3. The bot will reply with your **Chat ID**.

   **Example Output:**
   ```
   Your Chat ID: 987654321
   ```

![Get Chat ID with UserInfoBot](https://dummyimage.com/600x300/000/fff&text=UserInfoBot+Chat+ID)

---

## **Installation** 🛠️

Follow these simple steps to install **VaultCourier** and get it up and running in no time:

### **Step 1: Clone the Repository**
```bash
# Clone the repository
git clone https://github.com/yourusername/vaultcourier.git

# Navigate into the folder
cd vaultcourier
```

### **Step 2: Run the Installer**
```bash
# Make the installer executable
chmod +x vaultcourier.sh

# Run the installation script
./vaultcourier.sh
```

![Run Installer](https://dummyimage.com/600x300/000/fff&text=Run+Installer)

### **What the Installer Does** 🧐
1. Installs all required Python dependencies.
2. Configures your Telegram Bot Token and Chat ID.
3. Sets up the `vc` alias for easier usage.
4. Adds everything to your shell profile (e.g., `~/.bashrc` or `~/.zshrc`).

### **Step 3: Reload Your Terminal**
To activate the alias and environment variables, run:
```bash
source ~/.bashrc  # or ~/.zshrc if you're using Zsh
```

---

## **Usage** 📤
After installation, using VaultCourier is straightforward:

### **Send a File**
```bash
vc -f <file_path>
```
#### Example:
```bash
vc -f file.txt
```
Output:
```
[INFO] VaultCourier is starting...
[INFO] File 'file.txt' is being sent to Telegram...
[SUCCESS] File 'file.txt' has been successfully sent to Telegram.
[SUCCESS] VaultCourier finished its operation.
```

![Send File](https://dummyimage.com/600x300/000/fff&text=Send+File+Example)

### **Send a Folder**
```bash
vc -d <folder_path>
```
#### Example:
```bash
vc -d /path/to/folder
```
Output:
```
[INFO] VaultCourier is starting...
[INFO] Folder '/path/to/folder' has been zipped into 'folder.zip'.
[INFO] Message sent to Telegram: 'Here is the file you requested: folder.zip'
[SUCCESS] File 'folder.zip' has been successfully sent to Telegram.
[SUCCESS] Folder '/path/to/folder' has been successfully sent to Telegram.
[SUCCESS] VaultCourier finished its operation.
```

![Send Folder](https://dummyimage.com/600x300/000/fff&text=Send+Folder+Example)

---

## **Configuration** ⚙️
You can always update your Telegram Bot Token or Chat ID by editing your shell profile:

1. Open your shell profile:
   ```bash
   nano ~/.bashrc  # or ~/.zshrc for Zsh
   ```

2. Add or update these lines:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_bot_token"
   export TELEGRAM_CHAT_ID="your_chat_id"
   ```

3. Save and reload your profile:
   ```bash
   source ~/.bashrc
   ```

---

## **Dependencies** 📦
VaultCourier uses the following Python libraries:
- `requests` (for making HTTP requests to Telegram API)

All dependencies are automatically installed by the installer via `pip`.

---

## **File Structure** 🗂️
Here’s what the repository looks like:
```
vaultcourier/
├── vaultcourier.sh       # Installer script
├── vc/
│   ├── vaultcourier.py   # Main Python script
│   └── requirements.txt  # Dependencies
```

---

## **FAQs** ❓

### **1. What is Telegram Bot Token and Chat ID?**
- **Telegram Bot Token**: A unique key provided by @BotFather to authenticate your bot.
- **Chat ID**: The ID of your chat where the bot will send files. You can get it by messaging @userinfobot.

### **2. What if the `vc` command is not recognized?**
- Run `source ~/.bashrc` (or `~/.zshrc`) to reload your shell profile.
- Ensure the alias was added during installation.

### **3. Can I send large files?**
- Yes, Telegram supports files up to **2GB**.

---

## **Contributing** 🧱
Feel free to fork this repository, submit issues, or create pull requests. Contributions are always welcome! 💡

---

## **License** 📜
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Connect with Me** 🌐
- **GitHub**: [yourusername](https://github.com/yourusername)
- **Twitter**: [@yourhandle](https://twitter.com/yourhandle)
- **LinkedIn**: [Your Name](https://linkedin.com/in/yourprofile)

---

Made with ❤️ by **Spiuwirkid**

