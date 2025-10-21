from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import AudioPiped
from yt_dlp import YoutubeDL
import asyncio

API_ID = 1234567  # buraya senin api_id
API_HASH = "abc123def456"  # buraya senin api_hash
BOT_TOKEN = "1234567:ABCdefGHIjklMNOpqrSTUvwxYZ"  # buraya senin bot token
SESSION_STRING = "BURAYA_SESSION_STRING_GELECEK"  # bunu birazdan oluşturacağız

app = Client("musicbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client(SESSION_STRING, api_id=API_ID, api_hash=API_HASH)
call = PyTgCalls(user)

ydl_opts = {"format": "bestaudio/best", "quiet": True}

@call.on_stream_end()
async def on_end(_, update):
    chat_id = update.chat_id
    await app.send_message(chat_id, "🎵 Şarkı bitti!")

@app.on_message(filters.command("play") & filters.group)
async def play_music(_, message):
    if len(message.command) < 2:
        return await message.reply("🎶 Lütfen bir şarkı adı veya YouTube linki yaz bebeğim.")
    query = " ".join(message.command[1:])
    await message.reply(f"🔍 Arıyorum: **{query}**")

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
        url = info["url"]
        title = info["title"]

    await message.reply(f"🎧 Çalınıyor: **{title}**")
    await call.join_group_call(
        message.chat.id,
        AudioPiped(url),
    )

@app.on_message(filters.command("stop") & filters.group)
async def stop_music(_, message):
    await call.leave_group_call(message.chat.id)
    await message.reply("🛑 Müzik durduruldu.")

@app.on_message(filters.command("pause") & filters.group)
async def pause_music(_, message):
    await call.pause_stream(message.chat.id)
    await message.reply("⏸️ Durduruldu.")

@app.on_message(filters.command("resume") & filters.group)
async def resume_music(_, message):
    await call.resume_stream(message.chat.id)
    await message.reply("▶️ Devam ediyor.")

@app.on_message(filters.command("skip") & filters.group)
async def skip_music(_, message):
    await call.leave_group_call(message.chat.id)
    await message.reply("⏭️ Şarkı atlandı.")

async def main():
    await app.start()
    await user.start()
    await call.start()
    print("🎵 Kadim Music Bot çalışıyor!")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
