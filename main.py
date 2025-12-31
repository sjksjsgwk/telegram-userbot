from telethon import TelegramClient, events
import asyncio
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")

OWNER_ID = 7051750193
GROUP = -1001692874801

client = TelegramClient("session", api_id, api_hash)

running = False
task = None

async def spam_sil():
    global running
    while running:
        msg = await client.send_message(GROUP, "..")
        await asyncio.sleep(0.3)
        await msg.delete()
        await asyncio.sleep(10)

@client.on(events.NewMessage(pattern="/baslat"))
async def start_handler(event):
    global running, task
    if event.sender_id != OWNER_ID:
        return
    if running:
        await event.reply("⚠️ Zaten çalışıyor.")
        return
    running = True
    task = asyncio.create_task(spam_sil())
    await event.reply("✅ Başlatıldı.")

@client.on(events.NewMessage(pattern="/durdur"))
async def stop_handler(event):
    global running, task
    if event.sender_id != OWNER_ID:
        return
    if not running:
        await event.reply("⚠️ Zaten durmuş.")
        return
    running = False
    if task:
        task.cancel()
        task = None
    await event.reply("⛔ Durduruldu.")

client.start(phone=phone)
print("Userbot aktif")
client.run_until_disconnected()
