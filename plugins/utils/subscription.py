# utils/subscription.py
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from config import FORCE_SUB_IMAGE
from database.database import show_channels, get_channel_mode
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
async def get_channel_info(context: CallbackContext) -> tuple[dict, dict]:
    """Fetch channel names and invite links, cached for performance."""
    channels = await show_channels()
    channel_links = {}
    channel_names = {}
    for ch in channels:
        channel_id = ch["channel_id"]
        if ch["mode"] != "on":
            continue  # Skip channels with force-sub turned off
        try:
            bot_member = await context.bot.get_chat_member(chat_id=channel_id, user_id=context.bot.id)
            if bot_member.status not in ["member", "administrator", "creator"]:
                logger.warning(f"Bot is not a member of channel {channel_id}")
                channel_links[channel_id] = "https://t.me/+error"
                channel_names[channel_id] = "Unknown Channel"
                continue
        except Exception as e:
            logger.error(f"Error checking bot membership in channel {channel_id}: {e}")
            channel_links[channel_id] = "https://t.me/+error"
            channel_names[channel_id] = "Unknown Channel"
            continue

        try:
            chat = await context.bot.get_chat(chat_id=channel_id)
            channel_names[channel_id] = chat.title or "Unknown Channel"
            logger.info(f"Fetched name for channel {channel_id}: {channel_names[channel_id]}")
        except Exception as e:
            logger.error(f"Error fetching channel name for {channel_id}: {e}")
            channel_names[channel_id] = "Unknown Channel"

        try:
            invite_link = await context.bot.export_chat_invite_link(chat_id=channel_id)
            channel_links[channel_id] = invite_link
            logger.info(f"Generated invite link for channel {channel_id}: {invite_link}")
        except Exception as e:
            logger.error(f"Error generating invite link for channel {channel_id}: {e}")
            channel_links[channel_id] = "https://t.me/+error"

    return channel_links, channel_names

async def check_subscription(context: CallbackContext, user_id: int) -> bool:
    """Check if a user is subscribed to all required channels with mode 'on'."""
    channels = await show_channels()
    for ch in channels:
        channel_id = ch["channel_id"]
        if ch["mode"] != "on":
            continue  # Skip channels with force-sub turned off
        try:
            chat_member = await context.bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if chat_member.status not in ["member", "administrator", "creator"]:
                logger.info(f"User {user_id} not subscribed to channel {channel_id}. Status: {chat_member.status}")
                return False
        except Exception as e:
            logger.error(f"Error checking subscription for channel {channel_id} for user {user_id}: {e}")
            return False
    logger.info(f"User {user_id} is subscribed to all required channels")
    return True

async def prompt_subscription(update: Update, context: CallbackContext, user_id: int, edit_message: bool = False):
    """Prompt user to subscribe to required channels."""
    channel_links, channel_names = await get_channel_info(context)
    if not channel_links:
        if edit_message and update.callback_query:
            await update.callback_query.message.edit_text("No force-sub channels are currently active.")
        else:
            if update.message:
                await update.message.reply_text("No force-sub channels are currently active.")
            elif update.callback_query:
                await update.callback_query.message.reply_text("No force-sub channels are currently active.")
        return

    keyboard = [
        [InlineKeyboardButton(name, url=link) for link, name in zip(channel_links.values(), channel_names.values())],
        [InlineKeyboardButton("Check Subscription ✅", callback_data="check_subscription")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = "Please subscribe to the following channels to continue: 📢"
    
    try:
        if edit_message and update.callback_query:
            await update.callback_query.message.edit_media(
                media=telegram.InputMediaPhoto(FORCE_SUB_IMAGE, caption=caption),
                reply_markup=reply_markup
            )
        else:
            if update.message:
                await update.message.reply_photo(
                    photo=FORCE_SUB_IMAGE,
                    caption=caption,
                    reply_markup=reply_markup
                )
            elif update.callback_query:
                await update.callback_query.message.reply_photo(
                    photo=FORCE_SUB_IMAGE,
                    caption=caption,
                    reply_markup=reply_markup
                )
    except Exception as e:
        logger.error(f"Error sending Force Subscription image: {e}")
        if edit_message and update.callback_query:
            await update.callback_query.message.edit_text(
                text=caption,
                reply_markup=reply_markup
            )
        else:
            if update.message:
                await update.message.reply_text(
                    text=caption,
                    reply_markup=reply_markup
                )
            elif update.callback_query:
                await update.callback_query.message.reply_text(
                    text=caption,
                    reply_markup=reply_markup
                )
