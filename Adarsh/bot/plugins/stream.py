#(c) Adarsh-Goel
import os
import asyncio
from asyncio import TimeoutError
from Adarsh.bot import StreamBot
from Adarsh.utils.database import Database
from Adarsh.utils.human_readable import humanbytes
from Adarsh.vars import Var
from urllib.parse import quote_plus
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


MY_PASS = os.environ.get("MY_PASS",None)
pass_dict = {}
pass_db = Database(Var.DATABASE_URL, "ag_passwords")


@StreamBot.on_message((filters.regex("login🔑") | filters.command("login")) & ~filters.edited, group=4)
async def login_handler(c: Client, m: Message):
    try:
        try:
            ag = await m.reply_text("Now Send Me Password... 🔑\n\n\nYou Have To Buy Key From Onwer To Use Me, If you haven't buy it yet. \n\n(You can use /cancel command to cancel the process)")
            _text = await c.listen(m.chat.id, filters=filters.text, timeout=90)
            if _text.text:
                textp = _text.text
                if textp=="/cancel":
                   await ag.edit("Process Cancelled Successfully 😶‍🌫️")
                   return
            else:
                return
        except TimeoutError:
            await ag.edit("I can't wait more for password, try again")
            return
        if textp == MY_PASS:
            await pass_db.add_user_pass(m.chat.id, textp)
            ag_text = "YEAH! You Entered The Password Correctly 🔓.\n\nNOW PLEASE SEND ME THE FILE/VIDEO AGAIN..."
        else:
            ag_text = "Wrong Password 🔒\n\nPlease Press /LOGIN Command Again to continue.."
        await ag.edit(ag_text)
    except Exception as e:
        print(e)

@StreamBot.on_message((filters.private) & (filters.document | filters.video | filters.audio | filters.photo) & ~filters.edited, group=4)
async def private_receive_handler(c: Client, m: Message):
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(m.chat.id)
        if check_pass== None:
            await m.reply_text("You Have To Login First To Use Me, PLEASE PRESS /LOGIN Command To Login.")
            return
        if check_pass != MY_PASS:
            await pass_db.delete_user(m.chat.id)
            return
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ : \n\n Nᴀᴍᴇ : [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=m.chat.id,
                    text="𝚈𝙾𝚄 𝙰𝚁𝙴 𝙱𝙰𝙽𝙽𝙴𝙳../**",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return 
        except UserNotParticipant:
            await c.send_message(
                chat_id=m.chat.id,
                text="""<i>JOIN MY UPDATES CHANNEL TO USE ME..**\n\n**THIS IS VIP BOT, ONLY VIP CHANNEL SUBSCRIBERS CAN USE THIS BOT..!</i>""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("JOIN UPDATES CHANNEL.. (click here)", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="HTML"
            )
            return
        except Exception as e:
            await m.reply_text(e)
            await c.send_message(
                chat_id=m.chat.id,
                text="**𝙰𝙳𝙳 𝙵𝙾𝚁𝙲𝙴 𝚂𝚄𝙱 𝚃𝙾 𝙰𝙽𝚈 𝙲𝙷𝙰𝙽𝙽𝙴𝙻**",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    try:

        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{str(log_msg.message_id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        
        online_link = f"{Var.URL}{str(log_msg.message_id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
       
        
        

        msg_text ="""
<b>YOUR LINK IS GENERATED 🔮⚡

<b>📂 FILE NAME:- </b> <i><b>{}</b></i>

<b>🗃️ FILE SIZE:- </b> <i><b>{}</b></i>

<b>📥 DOWNLOAD LINK:- </b> <i><b>{}</b></i>

<b>🎥 WATCH ONLINE:- </b> <i><b>{}</b></i>



<b>♻️ THIS LINK IS PERMANENT AND WILL NOT EXPIRE ♻️\n\nThank you for being a premium user.💸😃</b>"""

        await log_msg.reply_text(text=f"**RᴇQᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uꜱᴇʀ ɪᴅ :** `{m.from_user.id}`\n**Stream ʟɪɴᴋ :** {stream_link}", disable_web_page_preview=True, parse_mode="Markdown", quote=True)
        await m.reply_text(
            text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(m)), online_link, stream_link),
            parse_mode="HTML", 
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⚡ WATCH ⚡", url=stream_link), #Stream Link
                                                InlineKeyboardButton('⚡ DOWNLOAD ⚡', url=online_link)]]) #Download Link
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**𝚄𝚜𝚎𝚛 𝙸𝙳 :** `{str(m.from_user.id)}`", disable_web_page_preview=True, parse_mode="Markdown")


@StreamBot.on_message(filters.channel & ~filters.group & (filters.document | filters.video | filters.photo) & ~filters.edited & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot, broadcast):
    if MY_PASS:
        check_pass = await pass_db.get_user_pass(broadcast.chat.id)
        if check_pass == None:
            await broadcast.reply_text("Login first using /login command \n don\'t know the password? request it from @Ishank_Kaushik")
            return
        if check_pass != MY_PASS:
            await broadcast.reply_text("Wrong password, login again")
            await pass_db.delete_user(broadcast.chat.id)
            return
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = f"{Var.URL}watch/{quote_plus(get_name(log_msg))}/{str(log_msg.message_id)}?hash={get_hash(log_msg)}"
        online_link = f"{Var.URL}{quote_plus(get_name(log_msg))}/{str(log_msg.message_id)}?hash={get_hash(log_msg)}"
        await log_msg.reply_text(
            text=f"**Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** `{broadcast.chat.title}`\n**Cʜᴀɴɴᴇʟ ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** {stream_link}",
            quote=True,
            parse_mode="Markdown"
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.message_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("⚡ WATCH ⚡", url=stream_link),
                     InlineKeyboardButton('⚡ DOWNLOAD ⚡', url=online_link)] 
                ]
            )
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(w.x)}s from {broadcast.chat.title}\n\n**Cʜᴀɴɴᴇʟ ID:** `{str(broadcast.chat.id)}`",
                             disable_web_page_preview=True, parse_mode="Markdown")
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#ᴇʀʀᴏʀ_ᴛʀᴀᴄᴇʙᴀᴄᴋ:** `{e}`", disable_web_page_preview=True, parse_mode="Markdown")
        print(f"Cᴀɴ'ᴛ Eᴅɪᴛ Bʀᴏᴀᴅᴄᴀsᴛ Mᴇssᴀɢᴇ!\nEʀʀᴏʀ:  **Give me edit permission in updates and bin Chanell{e}**")
