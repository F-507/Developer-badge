import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# سيرفر Flask لإبقاء البوت متصلاً 24/7 على Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# إعدادات ديسكورد
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        # مزامنة الأوامر المائلة (Slash Commands) تلقائياً عند التشغيل
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# أمر /badge يرسل تهنئة ورابط المطالبة المباشر
@bot.tree.command(name="badge", description="Get Active Developer Badge!")
async def badge(interaction: discord.Interaction):
    message = (
        " تهانينا! تم تسجيل نشاطك بنجاح.\n\n"
        " يمكنك المطالبة بالشارة بعد **24 إلى 48 ساعة** عبر الرابط التالي:\n"
        "https://discord.com/developers/active-developer"
    )
    await interaction.response.send_message(message)

# تشغيل السيرفر والبوت
keep_alive()
TOKEN = os.getenv("BOT_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("ERROR: BOT_TOKEN is missing!")
