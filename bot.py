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
USER_DIRECTORY_GROCERY: str = 'users-grocery'
USER_DIRECTORY_BUDGET: str = 'users-budget'

def create_check(args) -> bool:
    pass

def set_check(args) -> bool:
    pass

def edit_check(args) -> bool:
    pass

def spent_check(args) -> bool:
    pass

def total_check(args) -> bool:
    pass

# Stores the proper procedures and maps the necessary arguments
BUDGET_CHECK_MAPPER: dict = {
    "create" : create_check,
    "set": set_check,
    "edit": edit_check,
    "spent": spent_check,
    "total": total_check
}

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
    user_exists: bool = os.path.isfile(f"{USER_DIRECTORY_GROCERY}/{user_id}.csv")
    return user_exists

async def register_user(context, user_id: int):
    """Registers user into the proper directory"""
    users_file_path: str = os.path.join(USER_DIRECTORY_GROCERY, f"{user_id}.csv")
    with open(users_file_path, 'w') as file:
        print(f"Created file for {user_id}")

        # Fill out the columns
        file.write("Grocery_Item,Amount\n")
        await context.send("Added you to the Budget Bot! Welcome fella!")
    return

@bot.command()
async def add(context, *args):
    """
        Adds a grocery item to the database
        To run the command, use `!add_grocery_item <grocery_item> <optional: amount>`
    """

    if not args:
        await context.send("Please use this command with `!add <grocery item> <amount>`")
        return

    item_to_add: str = ""
    amount: int = 1

    try:
        amount = int(args[-1])
        item_to_add = " ".join(args[:-1])
    except ValueError:
        # Assume there is no number and use default values
        item_to_add = " ".join(args)

    if item_to_add == None or item_to_add == " " or item_to_add == "":
        await context.send("Please add an item to the grocery list.")
        return

    if amount <= 0:
        await context.send("Did you mean to send an amount of less than or equal to 0? Please try again.")
        return
    
    await user_check(context)

    user_id: int = context.author.id

    await add_item_to_grocery_list(context, item_to_add, user_id, amount)

# TODO: implement this with database
async def add_item_to_grocery_list(context, item: str, user_id, amount):
    # Database call
    # TODO: refactor this for PSQL call

    with open(f"{USER_DIRECTORY_GROCERY}/{user_id}.csv", 'a') as file:
        # Append to the file
        file.write(f"{item},{amount}\n")

    await context.send(f"Finished adding {amount} number of {item}(s)")

# Removes the grocery item from the grocery list provided
@bot.command()
async def remove(context, *args):
    if not args:
        await context.send("Please use this command with `!remove <grocery item> <amount>`")
        return

    item_to_remove: str = ""
    amount: int = sys.maxsize

    try:
        amount = int(args[-1])
        item_to_remove = " ".join(args[:-1])
    except ValueError:
        # Assume there is no number and use default values
        item_to_remove = " ".join(args)
    
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
    csv_file: str = f'./{USER_DIRECTORY_GROCERY}/{user_id}.csv'
    data = pandas.read_csv(csv_file)

    # Check if the item exists within the dataframe; if not, return message
    data_dict: dict = data.set_index("Grocery_Item").to_dict(orient="index")
    does_item_exist: bool = data_dict[item_to_remove] != None

    if (not does_item_exist):
        await context.send(f"{item_to_remove} does not exist within your grocery list.")
        return

    grocery_item_amount: int = int(data_dict[item_to_remove]['Amount'])

    if (grocery_item_amount < amount and amount != sys.maxsize):
        await context.send(f"You requested to remove {amount} {item_to_remove}(s) from the list, but you only have {grocery_item_amount}")
        return
    
    if (amount == sys.maxsize):
        amount = grocery_item_amount
        # grocery_item_amount = amount
    
    amount_to_set: int = grocery_item_amount - amount
    if (amount_to_set == 0):
        index_to_drop = data[((data.Grocery_Item == item_to_remove) & (data.Amount == grocery_item_amount))].index
        data = data.drop(index_to_drop)
        # data = data.drop(data["Grocery_Item" == item_to_remove].index)
    else:
        row_to_update = data.loc[data['Grocery_Item'] == item_to_remove].index[0]
        data.loc[row_to_update, 'Amount'] = amount_to_set
        # data.loc[data["Grocery_Item"] == item_to_remove, "Amount"] = amount_to_set

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
    data = pandas.read_csv(f'./{USER_DIRECTORY_GROCERY}/{user_id}.csv')

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

async def user_check_budget(context):
    user_id: int = context.author.id
    does_user_exist: bool = os.path.isfile(f"{USER_DIRECTORY_BUDGET}/{user_id}.csv")
    if not does_user_exist:
        await context.send("You aren't registered , silly! Make sure to run '!budget register' to register to the bot!")
        return

async def register_user_budget(context, *args):
    # Check if the user exists
    user_check_budget(context)

    # Add user to the proper area
    user_id: int = context.author.id
    users_file_path: str = os.path.join(USER_DIRECTORY_BUDGET, f"{user_id}.csv")
    with open(users_file_path, 'w') as file:
        print(f"Created file for {user_id}")

        # Fill out the columns
        file.write("Category,Budget,Total,Spent\n")
        await context.send("Added you to the Budget Bot! Welcome fella!")
    return

async def create_budget(context, *args):
    pass

async def set_budget(context, *args):
    print("NOT IMPLEMENTED YET")
    return

async def edit_budget(context, *args):
    print("NOT IMPLEMENTED YET")
    return

async def spent_budget(context, *args):
    print("NOT IMPLEMENTED YET")
    return

async def total_budget(context, *args):
    print("NOT IMPLEMENTED YET")
    return

async def clear_budget(context, *args):
    print("NOT IMPLEMENTED YET")
    return

BUDGET_METHOD_MAPPER: dict = {
    "register": register_user_budget,
    "create" : create_budget,
    "set": set_budget,
    "edit": edit_budget,
    "spent": spent_budget,
    "total": total_budget,
    "clear": clear_budget
}

@bot.command()
async def budget(context, *args):
    # Map the context of what we want to do for the budget
    # /budget register -> Creates a budget entry within the database for this specific user id
    # /budget create <budget-category> -> Creates a budget category for the user to add to if it does not already exist; if it does exist, will notify as a message
    # /budget set <budget-category> <amount> -> If the budget category exists, will set a budget limit for that category according to the limit that is passed in
    # /budget edit <budget-category> <amount> -> If the budget category exists and an amount exists, will edit the budget category limit to the amount passed in if the    
    # /budget spent <budget-category> <amount> -> Adds a total amount to the budget for that category; e.g. if I say /add bills 900, it'll add $900 to the bills category; if
    #    the user adds an expense that goes over the budget-category-total, will warn the user
    # /budget total <optional: budget-category> -> Does a running total of that budget category OR does a total breakdown of the entire budget; will display a fractional message
    #    of what the running total is; e.g. something akin to Groceries: 150/500
    # /budget clear -> Will clear the user's entire budget, but before doing so, will print out the entire budget history of the user
    
    # Check if a user
    if (not user_check(context.author.id)):
        await context.send("You aren't registered , silly! Make sure to run '!register' to register to the bot!")
        return

    # Parse through the context to find out what method is being called
    # TODO: figure out what kind of message I want to return to the user here to indicate what is available to use
    if not args:
        await context.send("Please use this command with `!budget <budget method>")
        return

    method: str = ""
    method_check = None

    # Parse through the args passed in:
    try:
        method = str(args[1])
        method_check = BUDGET_CHECK_MAPPER[method]
        is_valid_call: bool = method_check(args)
        if (not is_valid_call):
            # TODO: figure out what message to send to the user
            raise ValueError("Method Check did not resove properly.")
    except ValueError as error:
        print(str(error))
        # TODO: figure out what message to send to the user
        await context.send("Something went wrong! You may have used the command incorrectly!")
        return

    # Call the associated method
    budget_method = BUDGET_METHOD_MAPPER[method]
    budget_method(context, args)

if __name__ == "__main__":

    # Set the API key here

    # Run the bot
    bot.run(BOT_TOKEN)
