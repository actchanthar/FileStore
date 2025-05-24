import asyncio
import os
import random
import sys
import re
import string as rohit
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import *
from helper_func import *
from database.database import *
from database.db_premium import *
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize chat data cache
chat_data_cache = {}

BAN_SUPPORT = f"{BAN_SUPPORT}"
TUT_VID = f"{TUT_VID}"

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    is_premium = await is_premium_user(user_id)
    logger.info(f"Received /start command from user {user_id}")

    # Check if user is banned
    banned_users = await db.get_ban_users()
    if user_id in banned_users:
        logger.warning(f"User {user_id} is banned")
        return await message.reply_text(
            "<b>⛔️ You are Bᴀɴɴᴇᴅ from using this bot.</b>\n\n"
            "<i>Contact support if you think this is a mistake.</i>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Contact Support", url=BAN_SUPPORT)]]
            )
        )

    # Check if user is an admin and treat them as verified
    if user_id in await db.get_all_admins():
        verify_status = {
            'is_verified': True,
            'verify_token': None,
            'verified_time': time.time(),
            'link': ""
        }
    else:
        verify_status = await db.get_verify_status(user_id)

        # If TOKEN is enabled, handle verification logic
        if SHORTLINK_URL and SHORTLINK_API:
            if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
                await db.update_verify_status(user_id, is_verified=False)
                logger.info(f"User {user_id} verification expired")

            if "verify_" in message.text:
                try:
                    _, token = message.text.split("_", 1)
                    if verify_status['verify_token'] != token:
                        logger.warning(f"Invalid token for user {user_id}")
                        return await message.reply("Your token is invalid or expired. Try again by clicking /start.")
                    await db.update_verify_status(user_id, is_verified=True, verified_time=time.time())

                    current = await db.get_verify_count(user_id)
                    await db.set_verify_count(user_id, current + 1)
                    logger.info(f"User {user_id} verified successfully")
                    return await message.reply(
                        f"Bot ကိုအသုံးပြုနိုင်စွမ်းကို အောင်မြင်စွာရယူပြီးပါပြီ အချိန် {get_exp_time(VERIFY_EXPIRE)} အတွင်း၊ အချိန်ပြည့်သွားရင် Botအသုံးပြုနိုင်းစွမ်းပြန်ရယူရပါမည်။",
                        protect_content=False,
                        quote=True
                    )
                except Exception as e:
                    logger.error(f"Error processing verification for user {user_id}: {str(e)}")
                    return await message.reply("Error processing verification. Please try again.")

            if not verify_status['is_verified'] and not is_premium:
                token = ''.join(random.choices(rohit.ascii_letters + rohit.digits, k=10))
                await db.update_verify_status(user_id, verify_token=token, link="")
                try:
                    link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, f'https://telegram.dog/{client.username}?start=verify_{token}')
                    btn = [
                        [InlineKeyboardButton("• ᴏᴘᴇɴ ʟɪɴᴋ •", url=link),
                         InlineKeyboardButton('• ᴛᴜᴛoဇာတ်ကားကြည့်နည်း •', url=TUT_VID)],
                        [InlineKeyboardButton('• VIP or Premium ဝင်ရန် •', callback_data='premium')]
                    ]
                    logger.info(f"Generated verification link for user {user_id}")
                    return await message.reply(
                        f"𝗬𝗼𝘂𝗿 𝘁𝗼𝗸𝗲𝗻 𝗵𝗮𝘀 𝗲𝘅𝗽𝗶𝗿𝗲𝗱. 𝗣𝗹𝗲𝗮𝘀𝗲 𝗿𝗲𝗳𝗿𝗲𝘀𝗵 𝘆𝗼𝘂𝗿 𝘁𝗼𝗸𝗲𝗻 𝘁𝗼 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗲..\n\n<b> Video ကြည့်ရန် Bot ကိုသုံးနိုင်စွမ်း အချိန်ပြည့်သွားပါပြီဗျ!! Bot သုံးနိုင်စွမ်း\n\n : {get_exp_time(VERIFY_EXPIRE)}\nရယူရန် Open Link ကိုနှိပ်ပါ ၊ ထို့နောက် မလုပ်တတ်ရင် ᴛᴜᴛᴏʀɪᴀʟ ကိုနှိပ်ပါ။ Bot အသုံးပြုနိုင်စွမ်း {get_exp_time(VERIFY_EXPIRE)}</b>",
                        reply_markup=InlineKeyboardMarkup(btn),
                        protect_content=False,
                        quote=True
                    )
                except Exception as e:
                    logger.error(f"Error generating shortlink for user {user_id}: {str(e)}")
                    return await message.reply("Error generating verification link. Please try again.")

    # Check Force Subscription
    if not await is_subscribed(client, user_id):
        logger.info(f"User {user_id} not subscribed to required channels")
        return await not_joined(client, message)

    # File auto-delete time in seconds
    FILE_AUTO_DELETE = await db.get_del_timer()

    # Add user if not already present
    if not await db.present_user(user_id):
        try:
            await db.add_user(user_id)
            logger.info(f"Added new user {user_id} to database")
        except Exception as e:
            logger.error(f"Error adding user {user_id} to database: {str(e)}")

    # Handle normal message flow
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
            string = await decode(base64_string)
            argument = string.split("-")
            ids = []
            if len(argument) == 3:
                try:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                    ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
                except Exception as e:
                    logger.error(f"Error decoding IDs for user {user_id}: {str(e)}")
                    await message.reply_text("Invalid link format!")
                    return
            elif len(argument) == 2:
                try:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                except Exception as e:
                    logger.error(f"Error decoding ID for user {user_id}: {str(e)}")
                    await message.reply_text("Invalid link format!")
                    return

            temp_msg = await message.reply("<b>Please wait...</b>")
            try:
                messages = await get_messages(client, ids)
            except Exception as e:
                logger.error(f"Error getting messages for user {user_id}: {str(e)}")
                await message.reply_text("Something went wrong!")
                return
            finally:
                await temp_msg.delete()

            codeflix_msgs = []
            for msg in messages:
                caption = (CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html,
                                                 filename=msg.document.file_name) if bool(CUSTOM_CAPTION) and bool(msg.document)
                           else ("" if not msg.caption else msg.caption.html))

                reply_markup = msg.reply_markup if not DISABLE_CHANNEL_BUTTON else None

                try:
                    copied_msg = await msg.copy(chat_id=user_id, caption=caption, parse_mode=ParseMode.HTML,
                                                reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    codeflix_msgs.append(copied_msg)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    copied_msg = await msg.copy(chat_id=user_id, caption=caption, parse_mode=ParseMode.HTML,
                                                reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    codeflix_msgs.append(copied_msg)
                except Exception as e:
                    logger.error(f"Failed to send message to user {user_id}: {str(e)}")
                    continue

            if FILE_AUTO_DELETE > 0:
                notification_msg = await message.reply(
                    f"<b>❗️❗️❗️IMPORTANT❗️️❗️❗️ This file will be deleted in {get_exp_time(FILE_AUTO_DELETE)} . Please save or forward it to your saved messages before it gets deleted.\n\nဇာတ်ကားများသည် သတ်မှတ်ထားသော  {get_exp_time(FILE_AUTO_DELETE)}   မိနစ်အတွင်းပြန်ဖျက်ပါမည်။ ထို့ကြောင့် ဇာတ်ကားများကို Save Folder ထဲအမြန်ထည့်ထားပြီး ဇာတ်ကားများကိုကြည့်ပေးပါ။</b>"
                )

                await asyncio.sleep(FILE_AUTO_DELETE)

                for snt_msg in codeflix_msgs:
                    if snt_msg:
                        try:
                            await snt_msg.delete()
                        except Exception as e:
                            logger.error(f"Error deleting message {snt_msg.id} for user {user_id}: {str(e)}")

                try:
                    reload_url = (
                        f"https://t.me/{client.username}?start={message.command[1]}"
                        if message.command and len(message.command) > 1
                        else None
                    )
                    keyboard = InlineKeyboardMarkup(
                        [[InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!", url=reload_url)]]
                    ) if reload_url else None

                    await notification_msg.edit(
                        "<b>ʏᴏᴜʀ ᴠɪᴅᴇᴏ / ꜰɪʟᴇ ɪꜱ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ !!\n\nᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ᴅᴇʟᴇᴛᴇᴅ ᴠɪᴅᴇᴏ / ꜰɪʟᴇ 👇  ဗွီဒီယိုများကိုဖျက်လိုက်ပါပြီ ပြန်ကြည့်ရန် Get File Again ပြန်ယူရန် ကိုနှိပ်ပါ ။\n\n ဇာတ်ကားများမဖျက်ခင် Save Folder ထဲကိုပို့ထားပါ သို့မဟုတ် တစ်စုံတစ်ယောက်ကိုပို့ထားပါ။</b>",
                        reply_markup=keyboard
                    )
                except Exception as e:
                    logger.error(f"Error updating notification for user {user_id}: {str(e)}")
            return
        except IndexError:
            logger.error(f"Invalid base64 string format for user {user_id}")
            await message.reply_text("Invalid link format!")
            return
        except Exception as e:
            logger.error(f"Error processing message for user {user_id}: {str(e)}")
            await message.reply_text("Something went wrong!")
            return

    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("• ᴍᴏʀᴇ ᴄʜᴀɴɴᴇʟs •", url="https://t.me/addlist/E6xNJDDlvj43ZGU1")],
            [InlineKeyboardButton("• ᴀʙᴏᴜᴛ", callback_data="about"),
             InlineKeyboardButton('ʜᴇʟᴘ •', callback_data="help")]
        ]
    )
    await message.reply_photo(
        photo=START_PIC,
        caption=START_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=reply_markup,
        message_effect_id=5104841245755180586
    )
    logger.info(f"Sent start message to user {user_id}")

async def not_joined(client: Client, message: Message):
    user_id = message.from_user.id
    temp = await message.reply("<b><i>Checking Subscription...</i></b>")
    buttons = []
    count = 0
    logger.info(f"Checking subscription status for user {user_id}")

    try:
        all_channels = await db.show_channels()
        if not all_channels:
            logger.warning(f"No channels configured for force-sub for user {user_id}")
            await temp.delete()
            return await message.reply_text("No channels configured for subscription. Please contact support.")

        for chat_id in all_channels:
            mode = await db.get_channel_mode(chat_id)
            await message.reply_chat_action(ChatAction.TYPING)

            if not await is_sub(client, user_id, chat_id):
                try:
                    # Check cache first
                    if chat_id in chat_data_cache:
                        data = chat_data_cache[chat_id]
                    else:
                        # Fetch chat data and cache it
                        data = await client.get_chat(chat_id)
                        chat_data_cache[chat_id] = data

                    name = data.title
                    if mode == "on" and not data.username:
                        invite = await client.create_chat_invite_link(
                            chat_id=chat_id,
                            creates_join_request=True,
                            expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                        )
                        link = invite.invite_link
                    else:
                        link = f"https://t.me/{data.username}" if data.username else (
                            await client.create_chat_invite_link(
                                chat_id=chat_id,
                                expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                            )
                        ).invite_link

                    buttons.append([InlineKeyboardButton(text=name, url=link)])
                    count += 1
                    await temp.edit(f"<b>{'! ' * count}</b>")
                except Exception as e:
                    logger.error(f"Error with chat {chat_id} for user {user_id}: {str(e)}")
                    await temp.delete()
                    return await message.reply_text(
                        f"<b><i>! Error, Contact developer to solve the issues @actanibot</i></b>\n"
                        f"<blockquote expandable><b>Reason:</b> {e}</blockquote>"
                    )

        if count == 0:
            logger.info(f"User {user_id} is subscribed to all required channels")
            await temp.delete()
            return

        try:
            buttons.append([
                InlineKeyboardButton(
                    text='♻️ Try Again',
                    url=f"https://t.me/{client.username}?start={message.command[1] if message.command and len(message.command) > 1 else ''}"
                )
            ])
        except IndexError:
            pass

        await message.reply_photo(
            photo=FORCE_PIC,
            caption=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        logger.info(f"Sent force subscription message to user {user_id}")
    except Exception as e:
        logger.error(f"Error in not_joined for user {user_id}: {str(e)}")
        await temp.delete()
        return await message.reply_text(
            f"<b><i>! Error, Contact developer to solve the issues @actanibit</i></b>\n"
            f"<blockquote expandable><b>Reason:</b> {e}</blockquote>"
        )
    finally:
        await temp.delete()

@Bot.on_message(filters.command('myplan') & filters.private)
async def check_plan(client: Client, message: Message):
    user_id = message.from_user.id
    logger.info(f"Received /myplan command from user {user_id}")
    status_message = await check_user_plan(user_id)
    await message.reply(status_message)
    logger.info(f"Sent plan status to user {user_id}")

@Bot.on_message(filters.command('addpremium') & filters.private & admin)
async def add_premium_user_command(client: Client, message: Message):
    user_id = message.from_user.id
    logger.info(f"Received /addpremium command from user {user_id}")

    if len(message.command) != 4:
        logger.warning(f"Invalid /addpremium command format from user {user_id}")
        await message.reply_text(
            "Usage: /addpremium <user_id> <time_value> <time_unit>\n\n"
            "Time Units:\n"
            "s - seconds\n"
            "m - minutes\n"
            "h - hours\n"
            "d - days\n"
            "y - years\n\n"
            "Examples:\n"
            "/addpremium 123456789 30 m → 30 minutes\n"
            "/addpremium 123456789 2 h → 2 hours\n"
            "/addpremium 123456789 1 d → 1 day\n"
            "/addpremium 123456789 1 y → 1 year"
        )
        return

    try:
        target_user_id = int(message.command[1])
        time_value = int(message.command[2])
        time_unit = message.command[3].lower()

        # Validate time unit
        if time_unit not in ['s', 'm', 'h', 'd', 'y']:
            logger.warning(f"Invalid time unit '{time_unit}' from user {user_id}")
            await message.reply_text("❌ Invalid time unit. Use 's', 'm', 'h', 'd', or 'y'.")
            return

        # Call add_premium function
        expiration_time = await add_premium(target_user_id, time_value, time_unit)
        logger.info(f"Added premium for user {target_user_id}: {time_value} {time_unit}, expires {expiration_time}")

        # Notify the admin
        await message.reply_text(
            f"✅ User `{target_user_id}` added as a premium user for {time_value} {time_unit}.\n"
            f"Expiration Time: `{expiration_time}`"
        )

        # Notify the user
        try:
            await client.send_message(
                chat_id=target_user_id,
                text=(
                    f"🎉 Premium Activated!\n\n"
                    f"You have received premium access for `{time_value} {time_unit}`.\n"
                    f"Expires on: `{expiration_time}`"
                )
            )
            logger.info(f"Notified user {target_user_id} of premium activation")
        except UserIsBlocked:
            logger.warning(f"Cannot notify user {target_user_id}: User has blocked the bot")
            await message.reply_text(f"⚠️ Could not notify user {target_user_id}: They have blocked the bot")
        except InputUserDeactivated:
            logger.warning(f"Cannot notify user {target_user_id}: User account is deactivated")
            await message.reply_text(f"⚠️ Could not notify user {target_user_id}: Account is deactivated")
        except Exception as e:
            logger.error(f"Error notifying user {target_user_id}: {str(e)}")
            await message.reply_text(f"⚠️ Could not notify user {target_user_id}: {str(e)}")

    except ValueError as ve:
        logger.error(f"Invalid input for /addpremium from user {user_id}: {str(ve)}")
        await message.reply_text("❌ Invalid input. Please ensure user ID and time value are numbers.")
    except Exception as e:
        logger.error(f"Error processing /addpremium for user {user_id}: {str(e)}")
        await message.reply_text(f"⚠️ An error occurred: `{str(e)}`")

@Bot.on_message(filters.command('remove_premium') & filters.private & admin)
async def pre_remove_user(client: Client, message: Message):
    user_id = message.from_user.id
    logger.info(f"Received /remove_premium command from user {user_id}")

    if len(message.command) != 2:
        logger.warning(f"Invalid /remove_premium command format from user {user_id}")
        await message.reply_text("Usage: /remove_premium <user_id>")
        return

    try:
        target_user_id = int(message.command[1])
        if await remove_premium(target_user_id):
            await message.reply_text(f"✅ User `{target_user_id}` premium status removed.")
            logger.info(f"Removed premium status for user {target_user_id}")
        else:
            await message.reply_text(f"❌ User `{target_user_id}` is not a premium user.")
            logger.info(f"User {target_user_id} not found in premium database")
    except ValueError:
        logger.error(f"Invalid user_id for /remove_premium from user {user_id}")
        await message.reply_text("❌ User ID must be a number.")
    except Exception as e:
        logger.error(f"Error processing /remove_premium for user {user_id}: {str(e)}")
        await message.reply_text(f"⚠️ An error occurred: `{str(e)}`")

@Bot.on_message(filters.command('premium_users') & filters.private & admin)
async def list_premium_users_command(client: Client, message: Message):
    user_id = message.from_user.id
    logger.info(f"Received /premium_users command from user {user_id}")

    try:
        premium_user_list = await list_premium_users()
        if not premium_user_list:
            await message.reply_text("No active premium users found in the database.")
            logger.info(f"No premium users found for user {user_id}")
        else:
            await message.reply_text("\n\n".join(premium_user_list), parse_mode=ParseMode.HTML)
            logger.info(f"Sent premium users list to user {user_id}")
    except Exception as e:
        logger.error(f"Error listing premium users for user {user_id}: {str(e)}")
        await message.reply_text(f"⚠️ An error occurred: `{str(e)}`")

@Bot.on_message(filters.command("count") & filters.private & admin)
async def total_verify_count_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    logger.info(f"Received /count command from user {user_id}")
    try:
        total = await db.get_total_verify_count()
        await message.reply_text(f"Tᴏᴛᴀʟ ᴠᴇʀɪғɪᴇᴅ ᴛᴏᴋᴇɴs ᴛᴏᴅᴀʏ: <b>{total}</b>")
        logger.info(f"Sent verification count to user {user_id}: {total}")
    except Exception as e:
        logger.error(f"Error processing /count for user {user_id}: {str(e)}")
        await message.reply_text(f"⚠️ An error occurred: `{str(e)}`")

@Bot.on_message(filters.command('commands') & filters.private & admin)
async def bcmd(bot: Bot, message: Message):
    user_id = message.from_user.id
    logger.info(f"Received /commands command from user {user_id}")
    try:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close")]])
        await message.reply(text=CMD_TXT, reply_markup=reply_markup, quote=True)
        logger.info(f"Sent commands list to user {user_id}")
    except Exception as e:
        logger.error(f"Error processing /commands for user {user_id}: {str(e)}")
        await message.reply_text(f"⚠️ An error occurred: `{str(e)}`")