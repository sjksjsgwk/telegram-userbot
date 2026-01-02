import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ================== AYARLAR ==================
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")   # StringSession
OWNER_ID = int(os.environ.get("OWNER_ID"))
GROUP_ID = int(os.environ.get("GROUP_ID"))
# =============================================

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

running = False
task = None


async def spam_sil():
    global running
    while running:
        msg = await client.send_message(GROUP_ID, ".")
        await asyncio.sleep(0.2)
        await msg.delete()
        await asyncio.sleep(7)


@client.on(events.NewMessage(from_users=OWNER_ID))
async def handler(event):
    global running, task

    if event.raw_text == "/baslat":
        if not running:
            running = True
            task = asyncio.create_task(spam_sil())
            await event.reply("✅ Başladı")
        else:
            await event.reply("⚠️ Zaten çalışıyor")

    elif event.raw_text == "/durdur":
        if running:
            running = False
            if task:
                task.cancel()
            await event.reply("⛔ Durduruldu")
        else:
            await event.reply("⚠️ Zaten durmuş")


async def main():
    print("Userbot aktif")
    await client.run_until_disconnected()


client.start()
client.loop.run_until_complete(main())
