import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Set up bot with required intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# View class for the authentication button
class AuthView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistent view

    @discord.ui.button(label="Authenticate", style=discord.ButtonStyle.primary, emoji="🔐")
    async def auth_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Create DM with the user
        try:
            await interaction.user.send("Please authenticate using this link: https://gate-online.vercel.app")
            await interaction.response.send_message("Check your DMs for the authentication link!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I couldn't send you a DM. Please enable DMs from server members.", ephemeral=True)

# Slash command: /panel
@bot.tree.command(name="panel", description="Set up an authentication panel")
@commands.has_permissions(administrator=True)
async def panel(inter: discord.Interaction):
    embed = discord.Embed(
        title="Authentication Panel",
        description="Click the button below to receive an authentication link in your DMs.",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Powered by gate-online")
    view = AuthView()
    await inter.response.send_message(embed=embed, view=view)

# Slash command: /ping
@bot.tree.command(name="ping", description="Check the bot's latency")
async def ping(inter: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot latency: {latency}ms",
        color=discord.Color.green()
    )
    await inter.response.send_message(embed=embed)

# Run the bot
bot.run(TOKEN)
