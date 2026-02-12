Markdown
# ⛏️ GET SP: Ultimate Multi-Platform Miner

**GET SP** is a powerful Telegram bot designed to automate data and media extraction from various social media platforms, including Instagram, TikTok, YouTube, Pinterest, and Threads.

## 🚀 Features
* **Instagram**: Download profile media dumps in ZIP format (Powered by `instaloader`).
* **TikTok & YouTube**: Download videos and shorts in high quality, including metadata (Powered by `yt-dlp`).
* **Pinterest**: Extract images and full boards (Powered by `gallery-dl`).
* **Secure Config**: Stores your Telegram token and platform credentials locally in `miner_config.json`.
* **Anti-Ban Defense**: Integrated sleep settings to avoid `429 Too Many Requests` errors.

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/n0merc/get-sp.git](https://github.com/n0merc/get-sp.git)
cd get-sp
2. Install Dependencies
Bash
pip3 install python-telegram-bot instaloader yt-dlp gallery-dl imageio-ffmpeg
3. Setup FFmpeg (Mandatory for Video Merging)
Ensure ffmpeg is installed on your system path. On Windows, you can use:

Bash
pip install imageio-ffmpeg
🖥️ Usage
Run the script and follow the on-screen instructions to initialize your Telegram Bot Token:

Bash
python twinIG.py
Once the bot is active, use the /start command in Telegram to see the platform menu.

⚠️ Troubleshooting
Error 429: If you encounter "Too Many Requests," please switch your IP address (use a VPN or mobile hotspot) and wait.

Exit Status 101: Ensure you are providing valid URLs or that the platform hasn't temporarily blocked your connection.

⚖️ License
Distributed under the MIT License. See LICENSE for more information.

Developer
Developed by n0merc
