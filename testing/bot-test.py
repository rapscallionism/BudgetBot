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

test_cases: list[str] = [
    "Register when user does not exist, should be valid",
    "Register when user does exist, should not be valid",
    "Add grocery item to list when does not exist, should be valid",
    "Add grocery item to list when does exist, should be valid and increment",
    "Add grocery item to list with amount of 1, should be valid",
    "Add grocery item to list with amount of 0, should not be valid",
    "Add grocery item to list with amount of 1 and already exists, should be valid and increment",
    "Add grocery item multi-word with amount of 1, should be valid",
    "Add grocery item multi-word with amount of 0, should not be valid",
    "Remove grocery item from list does exist, should be valid and remove",
    "Remove grocery item from list does not exist, should not be valid and do nothing",
    "Remove grocery item from list by increment 1 does exist, should be valid remove 1",
    "Remove grocery item from list by increment 1 does exist but goes to 0, should be valid and remove entirely from the list",
    "Remove grocery item from list by increment 1 does not exist, should not be valid and do nothing",
]

if __name__ == "__main__":
    # Run the bot
    bot.run(BOT_TOKEN)