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
    deck_names = _extract_deck_names(*args)
    users = ctx.message.mentions

    print(deck_names)

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

    await ctx.channel.send("Decks sent to all players")

def _extract_deck_names(*args) -> List[str]:
    deck_names = []
    for arg in args:
        if is_serialized_user(arg):
            continue

        arg = arg.strip(',')
        deck_names.append(arg)

    return deck_names

bot.run(os.getenv('TOKEN'))