# (©)Codexbotz

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    logger.info(f"Received callback query: {data}")

    if data == "about":
        try:
            await query.message.edit_text(
                text=f"<b>○ Creator : <a href='tg://user?id={OWNER_ID}'>This Person</a>\n○ Language : <code>Python3</code>\n○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a></b>",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔒 Close", callback_data="close")
                        ]
                    ]
                )
            )
            logger.info("Displayed about information.")
        except Exception as e:
            logger.error(f"Error displaying about information: {e}")
    elif data == "close":
        try:
            await query.message.delete()
            try:
                await query.message.reply_to_message.delete()
            except Exception as e:
                logger.warning(f"Error deleting replied message: {e}")
            logger.info("Closed the message.")
        except Exception as e:
            logger.error(f"Error closing the message: {e}")
    else:
        logger.warning(f"Unhandled callback query: {data}")