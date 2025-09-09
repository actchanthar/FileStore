import os
from os import environ, getenv
import logging
from logging.handlers import RotatingFileHandler

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7828")
APP_ID = int(os.environ.get("APP_ID", "23034561"))
API_HASH = os.environ.get("API_HASH", "30b5ce6ea2bbbbc3fe5368bbce4d2db8")

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002772334487"))
OWNER = os.environ.get("OWNER", "When_the_night_falls_my_soul_se")
OWNER_ID = int(os.environ.get("OWNER_ID", "5062124930"))

PORT = os.environ.get("PORT", "8009")
DB_URI = os.environ.get("DATABASE_URL", "fuck")
DB_NAME = os.environ.get("DATABASE_NAME", "nyi")

FSUB_LINK_EXPIRY = int(os.getenv("FSUB_LINK_EXPIRY", "0"))
BAN_SUPPORT = os.environ.get("BAN_SUPPORT", "https://t.me/stranger77777777777")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "200"))

START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/cSB6pqwb/x.jpg")
FORCE_PIC = os.environ.get("FORCE_PIC", "https://i.ibb.co/5hBvK9Dq/x.jpg")

HELP_TXT = "<b><blockquote>ᴛʜɪs ɪs ᴀɴ ғɪʟᴇ Store @actanimemm\n\n❏ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs\n├/start : sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n├/about : ᴏᴜʀ Iɴғᴏʀᴍᴀᴛɪᴏɴ\n└/help : ʜᴇʟᴘ ʀᴇʟᴀᴛᴇᴅ ʙᴏᴛ\n\n sɪᴍᴘʟʏ ᴄʟɪᴄᴋ ᴏɴ ʟɪɴᴋ ᴀɴᴅ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴛʜᴀᴛs ɪᴛ.....!\n\n ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ <a href=https://t.me/actanibot>ACT</a></blockquote></b>"

ABOUT_TXT = "<b><blockquote>◈ ᴄʀᴇᴀᴛᴏʀ: <a href=https://t.me/actanibot>ACT</a>\n◈ ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href=https://t.me/actanimemm>ACT Anime MM</a>\n◈ ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ : <a href=https://t.me/actanimemm>ᴀɴɪᴍᴇ ᴄʀᴜɪsᴇ</a>\n◈ Hentai Channel: <a href=https://t.me/+v9h86AMQ5dowYWFl> Hentai</a>\n◈ ᴀᴅᴜʟᴛ ᴍᴀɴʜᴡᴀ : <a href=https://t.me/hentai_manhwammsub>ᴘᴏʀɴʜᴡᴀs</a>\n◈ ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=https://t.me/actanibot>ACT</a></blockquote></b>"

START_MSG = os.environ.get("START_MESSAGE", "<b>ʜᴇʟʟᴏ {first}\n\n<blockquote>Video / File သိမ်းပြီးပြန်ပို့တဲ့ bot ပါ။</blockquote></b>")
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "ʜᴇʟʟᴏ {first}\n\n<b> အောက်က Channel တစ်ခုချင်းဆီ ကို အရင် ဝင် Join ပေးပါ။ပြီးရင် Try Again ကို နှိပ်ပါ ဇာတ်ကား Video ကျလာပါလိမ့်မယ်ဗျ...အရင် မ Join ဘဲ မနှိပ်ပါနဲ့ Video မကျပါဘူး‌🥰</b>")

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

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "<b>• ʙʏ @Join_C_hannel</b>")
PROTECT_CONTENT = os.environ.get('PROTECT_CONTENT', "False") == "True"
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = " Bot ကိုတိုက်ရိုက်စာပို့လို့မရပါဘူး ကြော်ငြာကိစ္စစုံစမ်းလို့ပါက or Paid promotion @actanibot"

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
