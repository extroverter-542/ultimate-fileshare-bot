# (©)Codexbotz

from aiohttp import web
from plugins import web_server
import pyromod.listen
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from pyrogram.errors.exceptions.flood_420 import FloodWait
import sys
from datetime import datetime
import requests
import asyncio

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT, SHORTLINK_URL, SHORTLINK_API, VERIFY_EXPIRE, IS_VERIFY, TUT_VID, ADMINS

ascii_art = """
░█████╗░░█████╗░██████╗░███████╗██╗░░██╗██████╗░░█████╗░████████╗███╗░░██╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗╚══██╔══╝████╗░██║
██║░░╚═╝██║░░██║██║░░██║█████╗░░░╚███╔╝░██████╦╝██║░░██║░░░██║░░░██╔██╗██║
██║░░██╗██║░░██║██║░░██║██╔══╝░░░██╔██╗░██╔══██╗██║░░██║░░░██║░░░██║╚████║
╚█████╔╝╚█████╔╝██████╔╝███████╗██╔╝╚██╗██████╦╝╚█████╔╝░░░██║░░░██║░╚███║
░╚════╝░░╚════╝░╚═════╝░╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚══╝
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        while True:
            try:
                await super().start()
                usr_bot_me = await self.get_me()
                self.uptime = datetime.now()

                # Verify user
                user_id = usr_bot_me.id
                if not await verify_user(user_id):
                    self.LOGGER(__name__).info("User verification failed.")
                    return

                if FORCE_SUB_CHANNEL:
                    try:
                        link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                        if not link:
                            await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                            link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                        self.invitelink = link
                    except Exception as a:
                        self.LOGGER(__name__).warning(a)
                        self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                        self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel: {FORCE_SUB_CHANNEL}")
                        self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
                        sys.exit()
                try:
                    db_channel = await self.get_chat(CHANNEL_ID)
                    self.db_channel = db_channel
                    test = await self.send_message(chat_id=db_channel.id, text="Test Message")
                    await test.delete()
                except Exception as e:
                    self.LOGGER(__name__).warning(e)
                    self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
                    self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
                    sys.exit()

                self.set_parse_mode(ParseMode.HTML)
                self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/CodeXBotz")
                print(ascii_art)
                print("""Welcome to CodeXBotz File Sharing Bot""")
                self.username = usr_bot_me.username
                # web-response
                app = web.AppRunner(await web_server())
                await app.setup()
                bind_address = "0.0.0.0"
                await web.TCPSite(app, bind_address, PORT).start()
                break  # Exit the loop if successful

            except FloodWait as e:
                self.LOGGER(__name__).warning(f"FloodWait: Have to wait for {e.x} seconds.")
                await asyncio.sleep(e.x)  # Wait for the specified duration

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

async def verify_user(user_id: int) -> bool:
    if IS_VERIFY != "True":
        return True

    # Generate a short link for verification
    short_link = generate_short_link(user_id)

    # Send verification link to the user
    await bot.send_message(
        chat_id=user_id,
        text=f"Please verify yourself by clicking the following link: {short_link}\nThis link will expire in {VERIFY_EXPIRE // 3600} hours.\nTutorial: {TUT_VID}"
    )

    # Wait for the user to verify (simplified logic)
    return await wait_for_verification(user_id)

def generate_short_link(user_id: int) -> str:
    response = requests.get(f"{SHORTLINK_URL}/create", params={
        "api": SHORTLINK_API,
        "url": f"{SHORTLINK_URL}/verify?user_id={user_id}"
    })
    data = response.json()
    return data.get("shortlink", "Error generating link")

async def wait_for_verification(user_id: int) -> bool:
    await asyncio.sleep(VERIFY_EXPIRE)
    return True  # Assume user verified for simplicity

# Create a command to generate the verification link for users (admin only)
@Bot.on_message(filters.command("generate_link") & filters.user(ADMINS))
async def generate_link(client, message: Message):
    user_id = message.from_user.id
    short_link = generate_short_link(user_id)
    await message.reply_text(f"Generated shortlink: {short_link}")
