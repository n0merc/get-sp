import os
import shutil
import instaloader
import time
import random
import json
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- COLORS & CONFIG ---
R, G, Y, C, W = '\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;36m', '\033[0m'
CONFIG_FILE = 'miner_config.json'
DOWNLOAD_DIR = 'downloads'

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    # SyntaxWarning-ээс сэргийлж 'r' нэмэв
    print(rf"""{R}
  ________  ___________________      _________ __________ 
 /  _____/ /  _____/\__    ___/     /   _____/ \______   \
/   \  ___/   \  ___  |    |        \_____  \   |     ___/
\    \_\  \    \_\  \ |    |        /        \  |    |    
 \______  /\______  / |____|       /_______  /  |____|    
        \/        \/                       \/             
{C}
 ==========================================================
                LETS PLAY A FUN GAME BUDDY :D
                        by n0merc
 =========================================================={W}
    """)

if not os.path.exists(DOWNLOAD_DIR): os.makedirs(DOWNLOAD_DIR)

def setup_miner():
    if not os.path.exists(CONFIG_FILE):
        banner()
        print("--- FINAL SYSTEM INITIALIZATION ---")
        tg_token = input("Enter Telegram Bot Token: ")
        config = {"token": tg_token, "logins": {}}
        with open(CONFIG_FILE, 'w') as f: json.dump(config, f)
        return config
    with open(CONFIG_FILE, 'r') as f: return json.load(f)

config = setup_miner()
L = instaloader.Instaloader(user_agent="Mozilla/5.0")
L.sleep_settings = (40, 80)

# --- CORE FUNCTIONS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = (
        "--- GET CP FINAL MENU ---\n"
        "Available Platforms (Verified):\n"
        "1. Instagram\n"
        "2. TikTok (Video/Audio)\n"
        "3. Pinterest (Images/Boards)\n"
        "4. YouTube (Shorts/Videos)\n"
        "5. Threads\n\n"
        "Send the platform name to start."
    )
    await update.message.reply_text(menu)

async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    ud = context.user_data
    platforms = ["instagram", "tiktok", "pinterest", "youtube", "threads"]

    if text in platforms:
        ud['platform'] = text
        if text == "instagram" and text not in config.get('logins', {}):
            await update.message.reply_text(f"--- {text.upper()} LOGIN ---\nEnter Username:")
            ud['step'] = 'user'
        else:
            await update.message.reply_text(f"--- {text.upper()} READY ---\nEnter Target URL or Username:")
            ud['step'] = 'target'
        return

    if ud.get('step') == 'user':
        ud['tmp_u'] = text
        ud['step'] = 'pass'
        await update.message.reply_text(f"Enter password for {text}:")
        return

    if ud.get('step') == 'pass':
        p = ud['platform']
        config['logins'][p] = {"u": ud['tmp_u'], "p": text}
        with open(CONFIG_FILE, 'w') as f: json.dump(config, f)
        ud['step'] = 'target'
        await update.message.reply_text("Credentials saved. Now enter Target:")
        return

    if ud.get('step') == 'target':
        target = text
        plat = ud['platform']
        path = os.path.join(DOWNLOAD_DIR, f"{plat}_{int(time.time())}")
        
        await update.message.reply_text(f"--- EXTRACTION STARTED ---\nPlatform: {plat}\nTarget: {target}\nPlease wait...")

        try:
            if not os.path.exists(path): os.makedirs(path)

            if plat == "instagram":
                if "instagram" in config['logins']:
                    creds = config['logins']['instagram']
                    L.login(creds['u'], creds['p'])
                
                profile = instaloader.Profile.from_username(L.context, target)
                count = 0
                for post in profile.get_posts():
                    if count >= 5: break
                    L.download_post(post, target=path)
                    count += 1
                    time.sleep(random.randint(30, 60))

            elif plat in ["tiktok", "youtube"]:
                final_url = target
                if not target.startswith("http"):
                    if plat == "tiktok": final_url = f"https://www.tiktok.com/@{target}"
                    elif plat == "youtube": final_url = f"https://www.youtube.com/@{target}"
                
                # YouTube сувгийн линк бол /videos гэж нэмж өгвөл илүү тогтвортой
                if "youtube.com/@" in final_url and not final_url.endswith("/videos"):
                    final_url = final_url.rstrip('/') + "/videos"

                output_template = os.path.join(path, '%(title)s.%(ext)s')
                
                cmd = [
                    'yt-dlp', 
                    '-o', output_template, 
                    '--playlist-items', '1,2,3', # Эхний 3 видеог л авна
                    '--no-check-certificate',
                    '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    '--extract-audio' if "audio" in ud.get('mode', '') else '--format', 'bestvideo+bestaudio/best',
                    '--merge-output-format', 'mp4',
                    final_url
                ]
                subprocess.run(cmd, check=True)

            # Zip and Send
            archive_name = shutil.make_archive(path, 'zip', path)
            with open(archive_name, 'rb') as f:
                await update.message.reply_document(document=f, caption=f"SUCCESS: {plat.upper()} DUMP")
            
            # Cleanup
            if os.path.exists(archive_name): os.remove(archive_name)
            if os.path.exists(path): shutil.rmtree(path)
            ud.clear()

        except Exception as e:
            await update.message.reply_text(f"CRITICAL ERROR: {str(e)}")
            ud.clear()

if __name__ == '__main__':
    banner()
    app = Application.builder().token(config['token']).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_request))
    print("--- SYSTEM READY ---")
    app.run_polling()