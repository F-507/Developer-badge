import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread
import os

# سيرفر بسيط لإبقاء البوت شغال في Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# إعدادات البوت
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ⚠️ ايمتلك ضع ID الروم التي تريد للبوت الإرسال فيها هنا مكان الرقم 
CHANNEL_ID = 123456789012345678  

# تكرار إرسال الرسالة كل 168 ساعة (أسبوع كامل)
@tasks.loop(hours=168)
async def send_weekly_message():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("رسالة أسبوعية تلقائية لتنشيط البادج! 🚀")

@send_weekly_message.before_loop
async def before_weekly_message():
    await bot.wait_until_ready()

@bot.event
async def on_ready():
    print(f"تم التشغيل بنجاح: {bot.user}")
    if not send_weekly_message.is_running():
        send_weekly_message.start()

# تشغيل السيرفر والبوت
keep_alive()
bot.run(os.getenv("BOT_TOKEN"))
