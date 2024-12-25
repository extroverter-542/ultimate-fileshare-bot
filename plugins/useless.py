import logging
from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT
from datetime import datetime
from helper_func import get_readable_time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@Bot.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot: Bot, message: Message):
    try:
        now = datetime.now()
        delta = now - bot.uptime
        uptime = get_readable_time(delta.seconds)
        
        # Example of additional statistics
        total_users = len(await bot.get_chat_members_count(chat_id='your-group-or-channel-id'))
        
        await message.reply(BOT_STATS_TEXT.format(uptime=uptime, total_users=total_users))
        logger.info(f"Stats command executed by {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in stats command: {e}")
        await message.reply("Failed to retrieve stats.")

@Bot.on_message(filters.private & filters.incoming)
async def useless(_, message: Message):
    try:
        if USER_REPLY_TEXT:
            await message.reply(USER_REPLY_TEXT)
            logger.info(f"Replied to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in useless handler: {e}")