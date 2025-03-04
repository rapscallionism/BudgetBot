import sys
import discord
import os
import pandas
from models import Grocery
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
        file.write("Grocery_Item,Amount\n")
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
    
    await user_check(context)

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
    
    await user_check(context)

    await remove_item_from_grocery_list(context, item_to_remove, amount)

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
            # TODO: rename this variable and this structure of naming.. it looks mega terrible..
            # Grab the data for the grocery item and its amount
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
            
            # At this point, it means that we should be decrementing this by however much the user has passed in
            new_amount: int = grocery.amount - amount
            grocery_name: str = grocery.name

            # Remove the current line entirely and replace it with the new amount and grocery name
            file.write(f"{grocery_name},{new_amount}\n")

    await context.send(f"TODO: Unable to find Removing {item_to_remove}(s) from the grocery list")

@bot.command()
async def list(context):
    await user_check(context)
    await list_items(context)

async def list_items(context):
    formatted_string: str = "```\n# Grocery list\n"
    user_id: str = context.author.id
    data = pandas.read_csv(f'./users/{user_id}.csv')

    for row in data.itertuples(index=True, name="Row"):
        formatted_string += f"- {row.Grocery_Item} ({row.Amount})\n"

    formatted_string += "```"
    await context.send(formatted_string)

async def user_check(context):
    user_id: int = context.author.id
    does_user_exist: bool = check_if_user_exists(user_id)
    if not does_user_exist:
        await context.send("You aren't registered , silly! Make sure to run '!register' to register to the bot!")
        return


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
