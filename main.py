import os
from threading import Thread
from flask import Flask
import discord
from discord.ext import commands

# --- إنشاء سيرفر Flask لإبقاء البوت شغالاً على Render ---
app = Flask('')


@app.route('/')
def home():
  return 'Bot is online and active!'


def run():
  # استخدام Port الديناميكي الخاص بـ Render أو 8080 كافتراضي
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)


def keep_alive():
  t = Thread(target=run)
  t.daemon = True
  t.start()


# --- إعدادات ديسكورد ---
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ID الروم الخاص بك
CHANNEL_ID = 1550984275564961802


@bot.event
async def on_ready():
  print(f'Logged in as {bot.user}')

  # إرسال رسالة التفعيل للروم عند بدء التشغيل
  channel = bot.get_channel(CHANNEL_ID)
  if channel:
    await channel.send(
        ' البوت يعمل بنجاح الآن! اكتب الأمر `!badge` للحصول على الشارة.'
    )


@bot.command()
async def badge(ctx):
  """أمر تفاعلي لتنشيط شارة Active Developer"""
  await ctx.send(
      ' تم تسجيل نشاط البوت بنجاح! يمكنك التوجه لموقع ديسكورد واستلام الشارة خلال 24 ساعة.'
  )


# تشغيل سيرفر الويب أولاً ثم البوت
if __name__ == '__main__':
  keep_alive()
  token = os.environ.get('BOT_TOKEN')
  if token:
    bot.run(token)
  else:
    print('ERROR: BOT_TOKEN is missing from Environment Variables!')
