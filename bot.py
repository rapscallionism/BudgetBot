import discord
import os
import csv
from discord.ext import commands

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for message content

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot token
BOT_TOKEN = ***REMOVED***

# Directory to save the user data
USER_DIRECTORY: str = 'users'

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def list(context):
    """
        Lists out the grocery list for the user that currently exists
    """
    user_id: int = context.author.id
    does_user_exist: bool = check_if_user_exists(user_id)

    if not does_user_exist:
        await context.send("You aren't registered , silly! Make sure to run '!register' to register to the bot!")
        return

    grocery_list: str = await get_grocery_list(user_id)
    if grocery_list == "":
        await context.send("Looks like you don't have anything in your grocery list... you can add them by using '!add <grocery item>'")
        return

async def get_grocery_list(user_id):
    # Grab the entire CSV file
    with open(f"{USER_DIRECTORY}/{user_id}.csv", newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

    # If the rows is empty, then ignore it
    if not rows:
        return ""

    return rows

def format_to_markdown_table(row, column_widths):
    return "| " + " | ".join(f"{str(cell).ljust(width)}" for cell, width in zip(row, column_widths)) + " |"

@bot.command()
async def register(context):
    """
        Registers the user into the bot using their unique Discord ID
    """
    user_id: int = context.author.id
    does_user_exist: bool = check_if_user_exists(user_id)

    if does_user_exist:
        await context.send("You already exist, silly!")
        return
    
    await register_user(context, user_id)
    
def check_if_user_exists(user_id: int):
    # Check if the file path exists within the user directory
    user_exists: bool = os.path.isfile(f"{USER_DIRECTORY}/{user_id}.csv")
    return user_exists

async def register_user(context, user_id: int):
    """Registers user into the proper directory"""
    users_file_path: str = os.path.join(USER_DIRECTORY, f"{user_id}.csv")
    with open(users_file_path, 'w') as file:
        print(f"Created file for {user_id}")
        await context.send("Added you to the Budget Bot! Welcome fella!")
    return

@bot.command()
async def add(context, item_to_add: str, amount: int = 1):
    """
        Adds a grocery item to the database
        To run the command, use `!add_grocery_item <grocery_item> <optional: amount>`
    """

    if item_to_add == None:
        await context.send("Please add an item to the grocery list.")
        return

    if amount <= 0:
        await context.send("Did you mean to send an amount of less than or equal to 0? Please try again.")
        return
    
    user_id: int = context.author.id
    does_user_exist: bool = check_if_user_exists(user_id)
    if not does_user_exist:
        await context.send("You aren't registered , silly! Make sure to run '!register' to register to the bot!")
        return

    await add_item_to_grocery_list(context, item_to_add, user_id, amount)

# TODO: implement this with database
async def add_item_to_grocery_list(context, item: str, user_id, amount):
    # Database call
    # TODO: refactor this for PSQL call

    with open(f"{USER_DIRECTORY}/{user_id}.csv", 'a') as file:
        # Append to the file
        file.write("\n")
        file.write(f"{item},{amount}\n")

    await context.send(f"Finished adding {amount} number of {item}(s)")

# Removes the grocery item from the grocery list provided
@bot.command()
async def remove(context, item_to_remove: str, amount: int = 1):
    if item_to_remove == None:
        await context.send("Please provide an item to remove.")
        return
    
    if amount <= 0:
        await context.send("Did you mean to send an amount of less than or equal to 0? Please try again.")
        return

    remove_item_from_grocery_list(context, item_to_remove, amount)

async def remove_item_from_grocery_list(context, item_to_remove: str, amount: int):

    # Database call

    # Return and check

    await context.send(f"TODO: implement this. Removing {item_to_remove}(s) from the grocery list")


if __name__ == "__main__":
    # Run the bot
    bot.run(BOT_TOKEN)
