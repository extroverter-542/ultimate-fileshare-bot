# (©)CodeXBotz

import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()

# Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7615692183:AAHPQM7ABNs83nsHTau4GvyBG8alFlB_u98")

# Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "22281455"))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "dc3bf5521f4cd885f20e1fdd6aadd0ba")

# Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002333781701"))

# OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "8160777407"))

# Port
PORT = os.environ.get("PORT", "8080")

# Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://nico_music_bot:ahmed3434@cluster01.rnm5fc4.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "karasu_file_bot")

# Force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002437689157"))
JOIN_REQUEST_ENABLE = os.environ.get("JOIN_REQUEST_ENABLED", True)

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# Start message
START_PIC = os.environ.get("START_PIC", "https://envs.sh/JUW.jpg")
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link.")
try:
    ADMINS = []
    for x in (os.environ.get("ADMINS", "1683225887").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

# Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "<b><blockquote>›› ʜᴇʏ {mention} ×</blockquote>\nʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ, sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs.\n<blockquote>ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ : [ @Anime_Flux ]</blockquote></b>")

# Set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

# Set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

# Auto delete time in seconds.
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "300"))
AUTO_DELETE_MSG = os.environ.get("AUTO_DELETE_MSG", "This file will be automatically deleted in {time} seconds. Please ensure you have saved any necessary content before this time.")
AUTO_DEL_SUCCESS_MSG = os.environ.get("AUTO_DEL_SUCCESS_MSG", "Your file has been successfully deleted. Thank you for using our service. ✅")

# Set true if you want to disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

ADMINS.append(OWNER_ID)
ADMINS.append(8160777407)

# Shortlink service configuration
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "shortxlinks.com")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "aadb5c39c1319d8d8d70f935cb0eb3925a885a95")

# Verification configuration
VERIFY_EXPIRE = int(os.environ.get("VERIFY_EXPIRE", "64800"))
IS_VERIFY = os.environ.get("IS_VERIFY", "True")
TUT_VID = os.environ.get("TUT_VID", "https://t.me/+tutorial_video_link")

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)