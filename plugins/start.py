# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport
#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#

import os
from os import environ, getenv
import logging
from logging.handlers import RotatingFileHandler

# Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "8154426339")
APP_ID = int(os.environ.get("APP_ID", "25255650"))  # Your API ID from my.telegram.org
API_HASH = os.environ.get("API_HASH", "8eeadfa8f9b832d18657a63585b75bc0")  # Your API Hash from my.telegram.org

# Database channel ID
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002143185747"))  # Your db channel Id
OWNER = os.environ.get("OWNER", "When_the_night_falls_my_soul_se")  # Owner username without @
OWNER_ID = int(os.environ.get("OWNER_ID", "5062124930"))  # Owner id

# Port
PORT = os.environ.get("PORT", "8001")

# Database
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://act23:act23@cluster0.x1lrbcd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DATABASE_NAME", "actshare")

# Force subscription link expiry
FSUB_LINK_EXPIRY = int(os.getenv("FSUB_LINK_EXPIRY", "10"))  # 0 means no expiry
BAN_SUPPORT = os.environ.get("BAN_SUPPORT", "https://t.me/stranger77777777777")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "200"))

# Images
START_PIC = os.environ.get("START_PIC", "https://i.imghippo.com/files/fgmj5944fE.jpg")
FORCE_PIC = os.environ.get("FORCE_PIC", "https://i.imghippo.com/files/ZtkE2660GE.jpg")

# Token verification settings
TOKEN = True  # Enable token verification
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "ouo.io")  # Shortlink service URL
SHORTLINK_API = os.environ.get("SHORTLINK_API", "YOUR_OUO_IO_API_KEY")  # Replace with your ouo.io API key
VERIFY_EXPIRE = int(os.environ.get("VERIFY_EXPIRE", "600"))  # Token expiry time in seconds (e.g., 600 = 10 minutes)
TUT_VID = os.environ.get("TUT_VID", "https://t.me/actanimemm/3")  # Tutorial video link

# Help and About text
HELP_TXT = "<b><blockquote>ᴛʜɪs ɪs ᴀɴ ғɪʟᴇ Store @actanimemm\n\n❏ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs\n├/start : sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n├/about : ᴏᴜʀ Iɴғᴏʀᴍᴀᴛɪᴏɴ\n└/help : ʜᴇʟᴘ ʀᴇʟᴀᴛᴇᴅ ʙᴏᴛ\n\n sɪᴍᴘʟʏ ᴄʟɪᴄᴋ ᴏɴ ʟɪɴᴋ ᴀɴᴅ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴛʜᴀᴛs ɪᴛ.....!\n\n ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ <a href=https://t.me/actanibot>ACT</a></blockquote></b>"

ABOUT_TXT = "<b><blockquote>◈ ᴄʀᴇᴀᴛᴏʀ: <a href=https://t.me/actanibot>ACT</a>\n◈ ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href=https://t.me/actanimemm>ACT Anime MM</a>\n◈ ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ : <a href=https://t.me/actanimemm>ᴀɴɪᴍᴇ ᴄʀᴜɪsᴇ</a>\n◈ Hentai Channel: <a href=https://t.me/+v9h86AMQ5dowYWFl> Hentai</a>\n◈ ᴀᴅᴜʟᴛ ᴍᴀɴʜᴡᴀ : <a href=https://t.me/hentai_manhwammsub>ᴘᴏʀɴʜᴡᴀs</a>\n◈ ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=https://t.me/actanibot>ACT</a></blockquote></b>"

# Messages
START_MSG = os.environ.get("START_MESSAGE", "<b>ʜᴇʟʟᴏ {first}\n\n<blockquote> Video / File သိမ်းပြီးပြန်ပို့တဲ့ bot ပါ။</blockquote></b>")
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "ʜᴇʟʟᴏ {first}\n\n<b> Brother အောက်ကချာနယ် အရင်ဝင်ပါ ပြီးမှ ဝင်ပြီးရင် Reload ကိုနှိပ်ပါ အရင်မဝင်ဘဲမနှိပ်ပါနဲ့ ဖိုင်မရပါဘူး.</b>")

# Admin commands
CMD_TXT = """<blockquote><b>» ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:</b></blockquote>

<b>›› /dlt_time :</b> sᴇᴛ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ
<b>›› /check_dlt_time :</b> ᴄʜᴇᴄᴋ ᴄᴜʀʀᴇɴᴛ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ
<b>›› /dbroadcast :</b> ʙʀᴏᴀᴅᴄᴀsᴛ ᴅᴏᴄᴜᴍᴇɴᴛ / ᴠɪᴅᴇᴏ
<b>›› /ban :</b> ʙᴀɴ ᴀ ᴜꜱᴇʀ
<b>›› /unban :</b> ᴜɴʙᴀɴ ᴀ ᴜꜱᴇʀ
<b>›› /banlist :</b> ɢᴇᴛ ʟɪsᴛ ᴏꜰ ʙᴀɴɴᴇᴅ ᴜꜱᴇʀs
<b>›› /addchnl :</b> ᴀᴅᴅ ꜰᴏʀᴄᴇ sᴜʙ ᴄʜᴀɴɴᴇʟ
<b>›› /delchnl :</b> ʀᴇᴍᴏᴠᴇ ꜰᴏʀᴄᴇ sᴜʙ ᴄʜᴀɴɴᴇʟ
<b>›› /listchnl :</b> ᴠɪᴇᴡ ᴀᴅᴅᴇᴅ ᴄʜᴀɴɴᴇʟs
<b>›› /fsub_mode :</b> ᴛᴏɢɢʟᴇ ꜰᴏʀᴄᴇ sᴜʙ ᴍᴏᴅᴇ
<b>›› /pbroadcast :</b> sᴇɴᴅ ᴘʜᴏᴛᴏ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀs
<b>›› /add_admin :</b> ᴀᴅᴅ ᴀɴ ᴀᴅᴍɪɴ
<b>›› /deladmin :</b> ʀᴇᴍᴏᴠᴇ ᴀɴ ᴀᴅᴍɪɴ
<b>›› /admins :</b> ɢᴇᴛ ʟɪsᴛ ᴏꜰ ᴀᴅᴍɪɴs
"""

# Custom caption and content protection
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "<b>• ʙʏ @actanibot</b>")
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

# Disable channel button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

# Bot stats and user reply text
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = " Bot ကိုတိုက်ရိုက်စာပို့လို့မရပါဘူး ကြော်ငြာကိစ္စစုံစမ်းလို့ပါက or Paid promotion @actanibot"

# Admins
ADMINS = [5062124930]  # Add admin IDs here (e.g., OWNER_ID and others)

# Logging
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