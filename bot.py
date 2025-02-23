import discord
from discord.ext import commands

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for message content

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot token
BOT_TOKEN = ***REMOVED***

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def calculate(ctx, operation: str, *numbers: float):
    """Perform basic arithmetic operations."""
    if not numbers:
        await ctx.send("Please provide numbers to calculate.")
        return
    
    if operation == "add":
        result = sum(numbers)
    elif operation == "subtract":
        result = numbers[0] - sum(numbers[1:])
    elif operation == "multiply":
        result = 1
        for num in numbers:
            result *= num
    elif operation == "divide":
        try:
            result = numbers[0]
            for num in numbers[1:]:
                result /= num
        except ZeroDivisionError:
            await ctx.send("Division by zero is not allowed.")
            return
    else:
        await ctx.send("Unknown operation. Use add, subtract, multiply, or divide.")
        return

    await ctx.send(f"The result is: {result}")

# Run the bot
bot.run(BOT_TOKEN)
