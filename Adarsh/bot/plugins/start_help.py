# (c) adarsh-goel 
from Adarsh.bot import StreamBot
from Adarsh.vars import Var
import logging
logger = logging.getLogger(__name__)
from Adarsh.bot.plugins.stream import MY_PASS
from Adarsh.utils.human_readable import humanbytes
from Adarsh.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)
from pyrogram.types import ReplyKeyboardMarkup

                      
@StreamBot.on_message(filters.command('start') & filters.private & ~filters.edited)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started !!"
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL is not None:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "banned":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="**YOU ARE BANNED../**",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**JOIN MY UPDATES CHANNEL TO USE ME..**\n\n**THIS IS VIP BOT, ONLY VIP CHANNEL SUBSCRIBERS CAN USE THIS BOT..!**",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("JOIN UPDATES CHANNEL.. (click here)", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**𝙰𝙳𝙳 𝙵𝙾𝚁𝙲𝙴 𝚂𝚄𝙱 𝚃𝙾 𝙰𝙽𝚈 𝙲𝙷𝙰𝙽𝙽𝙴𝙻**",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return
        await m.reply_text(
            text="**Hii... 👋**\n\n**I AM  A PREMIUM TELEGRAM FILE (OR) VIDEO TO PERMANENT LINK GENERATOR BOT.**\n\n**I CAN GENERATE DIRECT DOWNLOAD LINK FOR ANY VIDEO/FILES FOR DOWNLOADING ONLINE AND FOR STREAMING..\n\nUSE /help FOR MORE DETAILS...\n\nSEND ME ANY VIDEO (OR) FILE TO SEE MY POWERS 🪄....**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🍁 DEVELOPER", url="https://t.me/ishank_kaushik"), InlineKeyboardButton("WEBSITE 🌐", url="https://www.ishank.ml")],
                   
                ]
            ),
            disable_web_page_preview=True
        )
    else:
        if Var.UPDATES_CHANNEL is not None:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "banned":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="**YOU ARE BANNED../**",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**JOIN MY UPDATES CHANNEL TO USE ME..**\n\n**THIS IS VIP BOT, ONLY VIP CHANNEL SUBSCRIBERS CAN USE THIS BOT..!**",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("JOIN UPDATES CHANNEL.. (click here)", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]                           
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**𝙰𝙳𝙳 𝙵𝙾𝚁𝙲𝙴 𝚂𝚄𝙱 𝚃𝙾 𝙰𝙽𝚈 𝙲𝙷𝙰𝙽𝙽𝙴𝙻**",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return

        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))

        file_size = None
        if get_msg.video:
            file_size = f"{humanbytes(get_msg.video.file_size)}"
        elif get_msg.document:
            file_size = f"{humanbytes(get_msg.document.file_size)}"
        elif get_msg.audio:
            file_size = f"{humanbytes(get_msg.audio.file_size)}"

        file_name = None
        if get_msg.video:
            file_name = f"{get_msg.video.file_name}"
        elif get_msg.document:
            file_name = f"{get_msg.document.file_name}"
        elif get_msg.audio:
            file_name = f"{get_msg.audio.file_name}"

        stream_link = "https://{}/{}".format(Var.FQDN, get_msg.message_id) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}".format(Var.FQDN,
                                     Var.PORT,
                                     get_msg.message_id)

        msg_text = "**YOUR LINK IS GENERATED...⚡\n\n📂 FILE NAME:-\n{}\n {}\n\n📥 DOWNLOAD LINK :- {}\n\n⚠️ THIS LINK IS PERMANENT AND WILL NOT EXPIRE\n\n ➖ @TFM_Server_Bot ➖**"
        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⚡ 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳 𝙽𝙾𝚆 ⚡", url=stream_link)]])
        )


@StreamBot.on_message(filters.command('help') & filters.private & ~filters.edited)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) Started !!"
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "banned":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="**YOU ARE BANNED../**",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="**JOIN MY UPDATES CHANNEL TO USE ME..**\n\n**THIS IS VIP BOT, ONLY VIP CHANNEL SUBSCRIBERS CAN USE THIS BOT..!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("JOIN UPDATES CHANNEL.. (click here)", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="**𝙰𝙳𝙳 𝙵𝙾𝚁𝙲𝙴 𝚂𝚄𝙱 𝚃𝙾 𝙰𝙽𝚈 𝙲𝙷𝙰𝙽𝙽𝙴𝙻**",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text="**┣⪼ SEND ME ANY FILE/VIDEO THEN I WILL GIVE YOU PERMANENT SHAREABLE LINK OF IT...\n\n┣⪼ THIS LINK CAN BE USED TO DOWNLOAD OR TO STREAM USING EXTERNAL VIDEO PLAYERS THROUGH MY SERVER.\n\n┣⪼ FOR STREAMING JUST COPY THE LINK AND PASTE IT IN YOUR VIDEO PLAYER TO START STREAMING.\n\n┣⪼ FOR MORE INFORMATION:- /about\n\n\nTHANKS FOR USING 🏖️**", 
  parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Buy Key To Use This Bot 🔑", url="https://t.me/ishank_kaushik")],
               
            ]
        )
    )

@StreamBot.on_message(filters.command('about') & filters.private & ~filters.edited)
async def about_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) Started !!"
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "banned":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="**YOU ARE BANNED../**",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="**JOIN MY UPDATES CHANNEL TO USE ME..**\n\n**THIS IS VIP BOT, ONLY VIP CHANNEL SUBSCRIBERS CAN USE THIS BOT..!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("JOIN UPDATES CHANNEL.. (click here)", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="**𝙰𝙳𝙳 𝙵𝙾𝚁𝙲𝙴 𝚂𝚄𝙱 𝚃𝙾 𝙰𝙽𝚈 𝙲𝙷𝙰𝙽𝙽𝙴𝙻**",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text="""<b>𝗦𝗢𝗠𝗘𝗧𝗛𝗜𝗡𝗚 𝗔𝗕𝗢𝗨𝗧 𝗠𝗘</b>
        
⚜️<b>MY NAME: <a href='https://t.me/tfm_server_bot'>TFM Server</a></b>\n
🔹<b>SUPPORT: <a href='https://t.me/ishank_kaushik'>Click Here</a></b>\n
🔸<b>LAST UPDATED: <a href='https://t.me/tfm_server_bot'>[03-July-2022]</a></b>\n
🔹<b>VERSION: 4.0.1</b>\n
🔸<b>SERVER: PREMIUM SERVER 💾</b>\n
🔹<b>SERVER LOCATION: UNITED STATES</b>\n
🔹<b>LANGUAGE: PYTHON</b>\n
🔸<b>BUY PREMIUM KEY: <a href='https://t.me/ishank_kaushik/chat'>Click Here</a></b>\n
🔹<b>WEBSITE: <a href='https://www.ishank.ml'>Click Here</a></b\n""",
  parse_mode="html",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Thanks For Reading ❤️", url="https://t.me/tfm_server_bot")],
               
            ]
        )
    )
