import random

from typing import List
from copy import copy
from re import search
random.seed()

serialized_user_regex = r"^<@![0-9]+>$"

def fisher_yates(items: list[str]) -> List[str]:
    items = copy(items)
    n = len(items)
    for i in range(n-1, 0, -1):
        j = random.randint(0, i)
        items[i], items[j] = items[j], items[i]

    return items

def get_ygo_top_deck_url(deck_name: str) -> str:
    deck_name = deck_name.replace(' ', '+')
    return f'http://yugiohtopdecks.com/decks/{deck_name}'

def get_assignment_message(user_name: str, deck_name: str) -> str:
    url = get_ygo_top_deck_url(deck_name)

    msg = (
        "==========\n"
        f"Hello {user_name}, this week you'll be piloting the \"{deck_name}\" archtype.\n"
        f"Try checking out some of the decks here: {url} (link may not actually exist lol)\n"
        "Good luck duelist!\n"
        "==========\n"
    )

    return msg

def is_serialized_user(arg: str) -> bool:
    return search(arg, serialized_user_regex) != None