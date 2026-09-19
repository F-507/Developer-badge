import os
from threading import Thread
from flask import Flask
import discord
from discord.ext import commands

# --- إعداد سيرفر Flask لإبقاء البوت شغالاً 24/7 ---
app = Flask('')


@app.route('/')
def home():
  return 'Bot is running!'


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()


# --- إعدادات بوت ديسكورد ---
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ID الروم الذي حددته
CHANNEL_ID = 1550984275564961802


@bot.event
async def on_ready():
  print(f'Logged in as {bot.user}')

  # إرسال أمور أو تفاعل للتحقق والحصول على الشارة (Active Developer Badge)
  channel = bot.get_channel(CHANNEL_ID)
  if channel:
    await channel.send(
        'البوت يعمل بنجاح الآن! استخدم الأمر `!badge` للحصول على شارة المطور.'
    )


@bot.command()
async def badge(ctx):
  """أمر تفاعلي لتنشيط شارة Active Developer"""
  await ctx.send(
      'تم تسجيل نشاط البوت بنجاح! يمكنك الآن التوجه إلى موقع ديسكورد واستلام الشارة خلال 24 ساعة.'
  )


# تشغيل خادم Flask ثم تشغيل البوت باستخدام التوكن من متغّيرات البيئة
keep_alive()
token = os.environ.get('BOT_TOKEN')
if token:
  bot.run(token)
else:
  print('ERROR: BOT_TOKEN is missing from Environment Variables!')
