import requests
import sys
import discord
from discord.ext import commands
import ctypes
import json
import os
import random
import asyncio
import datetime
import platform
from gtts import gTTS
import io
from colorama import init

init(autoreset=True)



# ================= KEY SYSTEM =================

# ================= START =================
print("""
     ▄ •▄ ▄▄▄  ▄• ▄▌       ▄▄▄· ▄▄▌  ▪  ▄▄▄ . ▐ ▄ 
    █▌▄▌▪▀▄ █·█▪██▌       ▐█ ▀█ ██•  ██ ▀▄.▀·•█▌▐█
    ▐▀▀▄·▐▀▀▄ █▌▐█▌      ▄█▀▀█ ██▪  ▐█·▐▀▀▪▄▐█▐▐▌
    ▐█.█▌▐█•█▌▐█▄█▌      ▐█ ▪▐▌▐█▌▐▌▐█▌▐█▄▄▌██▐█▌
    ·▀  ▀.▀  ▀ ▀▀▀  ▀▀▀   ▀  ▀ .▀▀▀ ▀▀▀ ▀▀▀ ▀▀ █▪
                                                   \n""")
token = input("MTE3NjE3NDc4MjMxNjgxODU1Mg.G0Mvva.VScEgnjHhu91er2OzlU55msT7j5h3_P6BcWWnw: ")
start_time = datetime.datetime.now(datetime.timezone.utc)
__version__ = "5.0.1"

with open("config/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

if "copycat" not in config:
    config["copycat"] = {"users": []}

prefix = config.get("prefix", ".")

bot = commands.Bot(
    command_prefix=prefix,
    self_bot=True,
    help_command=None
)

def save_config(cfg):
    with open("config/config.json", "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)

# ================= EVENTS =================
@bot.event
async def on_ready():
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"SelfBot v{__version__} - Kru_alien"
        )
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.id in config["copycat"]["users"] and message.content:
        await message.reply(message.content)

    if message.author != bot.user:
        return
    await bot.process_commands(message)

# ================= COMMANDS =================
@bot.command(aliases=["m"])
async def menu(ctx):
    await ctx.message.delete()
    await ctx.send(f"""
```yaml
☄️ Viet Area SelfBot 🌌
-----fun commands-----
.fun: xem danh sách lệnh fun
-----untils commands-----
.untils: xem danh sách lệnh untils
-----troll commands-----
.troll: xem danh sách lệnh troll
-----info tool-----
.info: xem thông tin tool
user: {bot.user}
version: v5.0.4
```""")
    await ctx.send("https://imgur.com/gI7Xa53")

@bot.command(aliases=["f"])
async def fun(ctx):
    await ctx.message.delete()
    await ctx.send(f"""
```yaml
☄️ Viet Area SelfBot 🌌
-----Fun command--(working:🟢)
.kiss <@user>: hôn ai đó
.dam <@user>: đấm ai đó
user: {bot.user}
version: v5.0.4
```""")
    await ctx.send("https://imgur.com/gI7Xa53")

@bot.command(aliases=["u"])
async def untils(ctx):
    await ctx.message.delete()
    await ctx.send(f"""
```yaml
☄️ Viet Area SelfBot 🌌
-----untils command--(working:🟢)
.tts <text>: chuyển text thành voice
.firstmessage: xem tin nhắn đầu trong kênh
user: {bot.user}
version: v5.0.4
```""")
    await ctx.send("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExeDRlYzNpYmhtbm85aXU0NmZraGJqdHM1OTl0bHY1NHFtdHpvNDBleSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TrVla4Z2PYEkU/giphy.gif")

@bot.command(aliases=["t"])
async def troll(ctx):
    await ctx.message.delete()
    await ctx.send(f"""
```yaml
☄️ Viet Area SelfBot 🌌
-----troll command--(working:🟢)
.spam <amount> <text>: spam nội dung
.nhay <amount> <@user>: nhay ai đó
.so <amount> <@user>: sớ ai đó
user: {bot.user}
version: v5.0.4
```""")
    await ctx.send("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExemRyeDdmcnlud2Y0YnE5eXppZGw4Z2ZmcndlYXJoZW81czB1dWwzdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/UC8DbMqXvkpd6/giphy.gif")

@bot.command(aliases=["i"])
async def info(ctx):
    await ctx.message.delete()
    await ctx.send(f"""
```yaml
☄️ Viet Area SelfBot 🌌
-----info tool------
Dev by Kru_alien
Sponsor: Viet Area, 𝓝𝓲𝓰𝓱𝓽 𝓒𝓵𝓾𝓫
user: {bot.user}
version: v5.0.4
```""")
    await ctx.send("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExemRyeDdmcnlud2Y0YnE5eXppZGw4Z2ZmcndlYXJoZW81czB1dWwzdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/UC8DbMqXvkpd6/giphy.gif")

# -------- utils --------
@bot.command()
async def tts(ctx, *, content=None):
    await ctx.message.delete()
    if not content:
        return
    tts = gTTS(text=content, lang="en")
    f = io.BytesIO()
    tts.write_to_fp(f)
    f.seek(0)
    await ctx.send(file=discord.File(f, "tts.wav"))

@bot.command()
async def firstmessage(ctx):
    await ctx.message.delete()
    try:
        async for message in ctx.channel.history(limit=1, oldest_first=True):
            link = f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{message.id}"
            await ctx.send(
                f"> Here is the link to the first message: {link}",
                delete_after=5
            )
            break
        else:
            await ctx.send(
                "> **[ERROR]**: No messages found in this channel.",
                delete_after=5
            )
    except Exception as e:
        await ctx.send(
            f"> **[ERROR]**: An error occurred while fetching the first message. `{e}`",
            delete_after=5
        )


# -------- fun --------
@bot.command()
async def kiss(ctx, user: discord.User = None):
    await ctx.message.delete()
    if not user:
        return
    await ctx.send(
        f"kiss {user.mention}\n"
        "https://media3.giphy.com/media/MQVpBqASxSlFu/giphy.gif"
    )

@bot.command()
async def dam(ctx, user: discord.User = None):
    await ctx.message.delete()
    if not user:
        return
    await ctx.send(
        f"đấm {user.mention}\n"
        "https://media1.giphy.com/media/NY3tXwOBUwQYq7lbXx/giphy.gif"
    )

@bot.command()
async def spam(ctx, amount: int = 1, *, message_to_send: str = "https://discord.gg/PKR7nM9j9U"):
    await ctx.message.delete()
    try:
        if amount <= 0 or amount > 10000:
            await ctx.send("> **[ERROR]**: Amount must be between 1 and 10000", delete_after=5)
            return
        for _ in range(amount):
            await ctx.send(message_to_send)
    except Exception:
        await ctx.send(
            '> **[ERROR]**: Invalid input\n> __Command__: `spam <amount> <message>`',
            delete_after=5
        )

# -------- nhay --------
@bot.command()
async def nhay(ctx, amount: int = 1, *, extra: str = ""):
    await ctx.message.delete()

    if amount < 1 or amount > 10000:
        await ctx.send("> **[ERROR]**: Số lượng phải từ 1 đến 10000.", delete_after=5)
        return

    filepath = "nhay.txt"

    if not os.path.isfile(filepath):
        await ctx.send(f"> **[ERROR]**: Không tìm thấy file `{filepath}`.", delete_after=7)
        return

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        await ctx.send(f"> **[ERROR]**: File `{filepath}` rỗng.", delete_after=7)
        return

    sent = 0
    for _ in range(amount):
        msg = random.choice(lines)
        if extra:
            msg = f"{msg} {extra}"
        await ctx.send(msg)
        sent += 1
        await asyncio.sleep(0.5)

    await ctx.send(f"> **Hoàn thành.** Đã gửi `{sent}` tin nhắn.", delete_after=6)
# -------- so --------
@bot.command()
async def so(ctx, amount: int = 1, *, extra: str = ""):
    await ctx.message.delete()

    if amount < 1 or amount > 10000:
        await ctx.send("> **[ERROR]**: Số lượng phải từ 1 đến 10000.", delete_after=5)
        return

    filepath = "so.txt"

    if not os.path.isfile(filepath):
        await ctx.send(f"> **[ERROR]**: Không tìm thấy file `{filepath}`.", delete_after=7)
        return

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        await ctx.send(f"> **[ERROR]**: File `{filepath}` rỗng.", delete_after=7)
        return

    sent = 0
    for _ in range(amount):
        msg = random.choice(lines)
        if extra:
            msg = f"{msg} {extra}"
        await ctx.send(msg)
        sent += 1
        await asyncio.sleep(0.5)

    await ctx.send(f"> **Hoàn thành.** Đã gửi `{sent}` tin nhắn.", delete_after=6)
# ================= RUN =================
bot.run(token, bot=False)
f"> **Hoàn thành.** Đã gửi `{sent}` tin nhắn."
# ================= RUN =================
bot.run(token, bot=False)
