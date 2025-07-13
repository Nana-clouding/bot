import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# 必要なインテントを設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# イベント: ボットが準備完了
@bot.event
async def on_ready():
    print(f"{bot.user} としてログインしました")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}個のコマンドを同期しました")
    except Exception as e:
        print(f"コマンドの同期に失敗しました: {e}")

# 認証ボタン用のビュークラス
class AuthView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # 永続的なビュー

    @discord.ui.button(label="認証", style=discord.ButtonStyle.primary, emoji="🔐")
    async def auth_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # ユーザーにDMを送信
        try:
            await interaction.user.send("以下のリンクで認証してください: https://gate-online.vercel.app")
            await interaction.response.send_message("DMに認証リンクを送信しました！", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("DMを送信できませんでした。サーバーメンバーからのDMを有効にしてください。", ephemeral=True)

# スラッシュコマンド: /panel
@bot.tree.command(name="panel", description="認証パネルを設置します")
@commands.has_permissions(administrator=True)
async def panel(inter: discord.Interaction):
    embed = discord.Embed(
        title="認証パネル",
        description="下のボタンをクリックして、DMで認証リンクを受け取ってください。",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Powered by gate-online")
    view = AuthView()
    await inter.response.send_message(embed=embed, view=view)

# スラッシュコマンド: /ping
@bot.tree.command(name="ping", description="ボットのレイテンシを確認します")
async def ping(inter: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"ボットのレイテンシ: {latency}ms",
        color=discord.Color.green()
    )
    await inter.response.send_message(embed=embed)

# ボットの起動
bot.run(TOKEN)
