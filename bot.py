import discord
import os
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
async def register(context):
    """
        Registers the user into the bot using their unique Discord ID
    """
    user_id: int = context.author.id
    does_user_exist: bool = check_if_user_exists(user_id)

    if does_user_exist:
        context.send("You already exist, silly!")
        return
    
    register_user(context, user_id)
    
def check_if_user_exists(user_id: int):
    # Check if the file path exists within the user directory
    user_exists: bool = os.path.isfile(f"{USER_DIRECTORY}/{user_id}.csv")
    return user_exists

def register_user(context, user_id: int):
    """Registers user into the proper directory"""
    users_file_path: str = os.path.join(USER_DIRECTORY, f"{user_id}.csv")
    with open(users_file_path, 'w') as file:
        print(f"Created file for {user_id}")
        context.send("Added you to the Budget Bot! Welcome fella!")
    return

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
    # TODO: refactor this for PSQL call

    # Check if the user already exists within the CSV
    user: int = context.author.id

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
