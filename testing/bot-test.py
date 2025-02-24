import discord
from discord.ext import commands

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for message content

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot token
BOT_TOKEN = 'MTM0MzM2NjM3NzYyMDI0NjY0MA.G51PC2.nMjZgJLTFKMqma-Q0mu751u5YfX1XLDAxwQaHU'

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Run the bot
bot.run(BOT_TOKEN)
