# (©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
import logging

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_shareable_link(client, post_message):
    """Generate a shareable link for a post message."""
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    return link, reply_markup

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start', 'users', 'broadcast', 'batch', 'genlink', 'stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        logger.warning(f"FloodWait: Sleeping for {e.value} seconds")
        await asyncio.sleep(e.value)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        logger.error(f"Error copying message: {e}")
        await reply_text.edit_text("Something went Wrong..!")
        return

    link, reply_markup = await generate_shareable_link(client, post_message)
    
    await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)

    if not DISABLE_CHANNEL_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except FloodWait as e:
            logger.warning(f"FloodWait: Sleeping for {e.value} seconds")
            await asyncio.sleep(e.value)
            await post_message.edit_reply_markup(reply_markup)
        except Exception as e:
            logger.error(f"Error editing reply markup: {e}")

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):
    if DISABLE_CHANNEL_BUTTON:
        return

    link, reply_markup = await generate_shareable_link(client, message)
    
    try:
        await message.edit_reply_markup(reply_markup)
    except FloodWait as e:
        logger.warning(f"FloodWait: Sleeping for {e.value} seconds")
        await asyncio.sleep(e.value)
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        logger.error(f"Error editing reply markup: {e}")