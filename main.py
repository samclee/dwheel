import discord
import os

from discord.ext import commands
from typing import List, Tuple, Union
from utils import fisher_yates, get_assignment_message, is_serialized_user
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix=">")

@bot.event
async def on_ready():
    print('Let\'s Rev it Up!')

@bot.command()
async def deck_assign(ctx, *args):
    deck_names = _validate_deck_names(*args)
    if isinstance(deck_names, str):
        await ctx.channel.send(deck_names)
        return
    
    users = ctx.message.mentions

    # validate count for both
    if len(deck_names) < len(users):
        await ctx.channel.send("Too few decks for listed players!")
        return

    # assign decks
    deck_names = fisher_yates(deck_names)
    for i in range(0, len(users)):
        user = users[i]
        deck_name = deck_names[i]

        print(f"Sending assignment to {user.name}")
        await user.send(get_assignment_message(user.name, deck_name))

    await ctx.channel.send("Decks sent to all player")

def _validate_deck_names(*args)->Union[List[str], str]:
    if len(args) == 0:
        return "Too few arguments given!"

    deck_names_str = args[0]
    
    # validate deck names
    if deck_names_str.count(",") == 0:
        return "Invalid deck names list!"

    deck_names = deck_names_str.split(',')
    deck_names = list(map(lambda x: x.strip(), deck_names))
    deck_names = list(filter(lambda x: len(x) > 0, deck_names))
    print(deck_names)

    print("Validation succeeded")
    return deck_names

bot.run(os.getenv('TOKEN'))