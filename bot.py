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
BOT_TOKEN = 'MTMzMzg5MzcxOTExOTYzMDM4Nw.Ghp_ZI.0DO5yKLkXji1KjRIYce-UKV_eD1C3KH-SfroUY'

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

async def remove_item_from_grocery_list(context, item_to_remove: str, amount: int = sys.maxsize):
    user_id: str = context.author.id
    csv_file: str = f'./users/{user_id}.csv'
    data = pandas.read_csv(csv_file)

    # Check if the item exists within the dataframe; if not, return message
    data_dict: dict = data.set_index("Grocery_Item").to_dict(orient="index")
    does_item_exist: bool = data_dict[item_to_remove] != None

    if (not does_item_exist):
        await context.send(f"{item_to_remove} does not exist within your grocery list.")
        return
    
    grocery_item_amount: int = int(data_dict[item_to_remove])
    
    if (grocery_item_amount < amount):
        await context.send(f"You requested to remove {amount} {item_to_remove}(s) from the list, but you only have {grocery_item_amount}")
        return
    
    amount_to_set: int = grocery_item_amount - amount
    if (amount_to_set == 0):
        data = data[data[item_to_remove] != item_to_remove]
    else:
        data.loc[data["Grocery_Item"] == item_to_remove, "Amount"] = amount_to_set

    data.to_csv(csv_file, index=False)
    await context.send(f"Finished removing {amount} {item_to_remove}(s) from the grocery list.")
    return

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
