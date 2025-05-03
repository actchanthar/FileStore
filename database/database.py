# database/database.py
# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport

from pymongo import MongoClient
from config import DB_URI, DB_NAME

# Initialize MongoDB client
client = MongoClient(DB_URI)
db = client[DB_NAME]

async def get_ban_users():
    """Return a list of banned user IDs."""
    banned_users = await db.banned_users.find().to_list(length=None)
    return [user["user_id"] for user in banned_users]

async def add_user(user_id):
    """Add a new user to the database."""
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

async def present_user(user_id):
    """Check if a user exists in the database."""
    user = await db.users.find_one({"user_id": user_id})
    return bool(user)

async def get_del_timer():
    """Get the file auto-delete timer (in seconds)."""
    settings = await db.settings.find_one({"type": "delete_timer"})
    return settings.get("value", 600) if settings else 600  # Default: 10 minutes

async def show_channels():
    """Return a list of force-sub channel IDs."""
    channels = await db.channels.find().to_list(length=None)
    return [channel["chat_id"] for channel in channels]

async def get_channel_mode(chat_id):
    """Get the mode ('on' or 'off') for a force-sub channel."""
    channel = await db.channels.find_one({"chat_id": chat_id})
    return channel.get("mode", "off") if channel else "off"

async def req_user_exist(chat_id, user_id):
    """Check if a user has a pending join request for a channel."""
    request = await db.join_requests.find_one({"chat_id": chat_id, "user_id": user_id})
    return bool(request)

async def admin_exist(user_id):
    """Check if a user is an admin."""
    admin = await db.admins.find_one({"user_id": user_id})
    return bool(admin)

async def db_verify_status(user_id):
    """Get the verification status of a user."""
    user = await db.users.find_one({"user_id": user_id})
    if not user:
        return {"is_verified": False, "verify_token": "", "verified_time": 0, "link": ""}
    return {
        "is_verified": user.get("is_verified", False),
        "verify_token": user.get("verify_token", ""),
        "verified_time": user.get("verified_time", 0),
        "link": user.get("link", "")
    }

async def db_update_verify_status(user_id, data):
    """Update the verification status of a user."""
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {
            "is_verified": data["is_verified"],
            "verify_token": data["verify_token"],
            "verified_time": data["verified_time"],
            "link": data["link"]
        }},
        upsert=True
    )