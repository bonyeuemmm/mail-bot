import os
import json
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
CLIENT_ID = None

if os.path.exists("config.json"):
    with open("config.json", "r", encoding="utf-8") as f:
        try:
            config = json.load(f)
            if not TOKEN:
                TOKEN = config.get("TOKEN")
            CLIENT_ID = config.get("CLIENT_ID")
        except json.JSONDecodeError:
            pass

class RegEmailModal(discord.ui.Modal, title="Đăng Ký Khởi Tạo Email"):
    email_name = discord.ui.TextInput(
        label="Tên Email (Prefix)",
        placeholder="Nhập tên email muốn tạo...",
        required=True,
        max_length=50
    )
    email_password = discord.ui.TextInput(
        label="Mật Khẩu Email",
        placeholder="Nhập mật khẩu...",
        required=True,
        style=discord.TextStyle.short,
        min_length=6
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        username = self.email_name.value
        password = self.email_password.value
        
        await asyncio.sleep(2)
        
        full_email = f"{username}@gmail.com"
        
        embed = discord.Embed(
            title="Khởi Tạo Email Thành Công",
            color=discord.Color.green()
        )
        embed.add_field(name="Email", value=full_email, inline=False)
        embed.add_field(name="Mật khẩu", value=password, inline=False)
        embed.set_footer(text="Hệ thống đăng ký tự động")
        
        await interaction.followup.send(embed=embed, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message("Đã xảy ra lỗi trong quá trình xử lý.", ephemeral=True)

class BotClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        app_id = int(CLIENT_ID) if CLIENT_ID and str(CLIENT_ID).isdigit() else None
        super().__init__(
            command_prefix="!", 
            intents=intents,
            application_id=app_id
        )

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"Bot logged in as {self.user} (Client ID: {self.application_id})")

bot = BotClient()

@bot.tree.command(name="muagmail", description="Yêu cầu khởi tạo tài khoản Gmail mới")
async def muagmail(interaction: discord.Interaction):
    modal = RegEmailModal()
    await interaction.response.send_modal(modal)

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("Lỗi: Không tìm thấy DISCORD_TOKEN trong Environment Variable hoặc config.json!")
    bot.run(TOKEN)