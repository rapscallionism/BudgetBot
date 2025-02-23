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

@bot.command()
async def add(context, item_to_add: str, amount: int = 0):
    """
        Adds a grocery item to the database
        To run the command, use `!add_grocery_item <grocery_item> <optional: amount>`
    """

    if item_to_add == None:
        await context.send("Please add an item to the grocery list.")

    await add_item_to_grocery_list(context, item_to_add)

# TODO: implement this with database
async def add_item_to_grocery_list(context, item: str, amount: int = 0):
    # Database call

    # Return and check

    await context.send(f"TODO: implement this. Adding {amount} numer of {item}(s)")

# Removes the grocery item from the grocery list provided
@bot.command()
async def remove(context, item_to_remove: str):
    if item_to_remove == None:
        await context.send("Please provide an item to remove.")

async def remove_item_from_grocery_list(context, item_to_remove: str):

    # Database call

    # Return and check

    await context.send(f"TODO: implement this. Removing {item_to_remove}(s) from the grocery list")

# Run the bot
bot.run(BOT_TOKEN)
