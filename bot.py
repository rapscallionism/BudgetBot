import sys
import discord
import os
import csv
from models import Grocery
from discord.ext import commands

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for message content

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot token
BOT_TOKEN = 'MTMzMzg5MzcxOTExOTYzMDM4Nw.Ghp_ZI.0DO5yKLkXji1KjRIYce-UKV_eD1C3KH-SfroUY'

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

    await get_grocery_list(context, user_id)
    
async def get_grocery_list(context, user_id):
    # Grab the entire CSV file
    # TODO: refactor this, this is terrible way to do it
    formatted_message: str = ""
    lines: list[str] = []
    with open(f"{USER_DIRECTORY}/{user_id}.csv", newline='', encoding='utf-8') as csv_file:
        lines = csv_file.readlines()
        if not lines:
            await context.send("Looks like you don't have anything in your grocery list... you can add them by using '!add <grocery item>'")
            return

        csv_file.close()

    # Trim off the header
    lines = lines[1:]

    formatted_message = format_to_markdown_table(lines)

    await context.send(formatted_message)

def format_to_markdown_table(lines: list) -> str:
    """
        Format to proper markdown
    """
    formatted_string: str = "```"
    formatted_string += "# Grocery List\n"

    for row in lines:
        # Trim off the \r\n and turn it into comma sep.
        row = row.replace("\r", "").replace("\n", "").split(",")

        # TODO: find a way to counter the invariance of doing this, tight coupling with impl.
        grocery = Grocery.Grocery(row[0], row[1])
        formatted_string += grocery.format_to_markdown_string()

    # Markdown (?)
    formatted_string += "```"
    
    return formatted_string

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

        # Fill out the columns
        file.write("Grocery Item,Amount\n")
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
        file.write(f"{item},{amount}\n")

    await context.send(f"Finished adding {amount} number of {item}(s)")

# Removes the grocery item from the grocery list provided
@bot.command()
async def remove(context, item_to_remove: str, amount: int = sys.maxsize):
    if item_to_remove == None:
        await context.send("Please provide an item to remove.")
        return
    
    if amount <= 0 :
        await context.send("Did you mean to send an amount of less than or equal to 0? Please try again.")
        return
    
    user_id: int = context.author.id
    does_user_exist: bool = check_if_user_exists(user_id)
    if not does_user_exist:
        await context.send("You aren't registered , silly! Make sure to run '!register' to register to the bot!")
        return

    await remove_item_from_grocery_list(context, user_id, item_to_remove, amount)

async def remove_item_from_grocery_list(context, user_id, item_to_remove: str, amount: int = sys.maxsize):

    # Database call
    with open(f"{USER_DIRECTORY}/{user_id}.csv", "r+") as file:
        lines = file.readlines()
    
        # Trim off the header
        lines = lines[1:]

        # Loop through and double check if the item is what was provided to remove
        for row in lines:
            # Trim off the \r\n and turn it into comma sep.
            row = row.replace("\r", "").replace("\n", "").split(",")

            # TODO: find a way to counter the invariance of doing this, tight coupling with impl.
            grocery = Grocery.Grocery(row[0], row[1])

            if (grocery.name != item_to_remove):
                continue

            if (int(grocery.amount) < int(amount)) and amount != sys.maxsize:
                await context.send(f"""Looks like you're trying to remove {amount} more than 
                            just what you have listed {grocery.amount}. Please try again.""")
                return

            # If it's calling this amount, it means default, delete the entire grocery item off the list
            if (amount == sys.maxsize):
                print(f"Removing {grocery.name} from the list...")
                file.write("\n")
                await context.send(f"Removed {grocery.name} from the list.")
                return
            
            if (grocery.amount - amount == 0):
                print(f"Removing {amount} from {grocery.name} will remove it entirely. Removing it from the list..")
                file.write("\n")
                await context.send(f"Removed {grocery.name} from the list.")
                return

    await context.send(f"TODO: implement this. Removing {item_to_remove}(s) from the grocery list")

@bot.command()
async def empty(context):
    # Prelim check 
    user_id: int = context.author.id
    does_user_exist: bool = check_if_user_exists(user_id)
    if not does_user_exist:
        await context.send("You aren't registered , silly! Make sure to run '!register' to register to the bot!")
        return
    
async def empty_grocery_list(context):
    """
        Fully empties out the grocery list but keeps the user registered
    """

    pass

def grab_api_key(file: str) -> str:
    pass

if __name__ == "__main__":

    # Set the API key here

    # Run the bot
    bot.run(BOT_TOKEN)
