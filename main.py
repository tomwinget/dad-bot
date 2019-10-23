import os
import re
import random
import requests
import discord

TOKEN = os.environ['dadToken']
client = discord.Client()
client.login(TOKEN)

dadPattern = r"^(?:i’m|i'm|im|i am) ?a? ([^\.\,\n]*)"
alphaPattern = r"^(\D+?\s+\D+?)+$"
loudMessages = [
    'Now calm down {user}!',
    'No yelling in the house {user}!',
    'Lower your voice {user}!',
    'You\'re being too loud {user}!'
]


def get_joke() -> str:
    '''Makes request to dadjoke service and returns a formatted joke string
    '''
    response = requests.get(
        'https://icanhazdadjoke.com/',
        headers={
            'Accept': 'text/plain',
            'User-Agent': 'dad-bot (github.com/tomwinget/dad-bot)'
        }
    )
    response.raise_for_status()
    return response.text


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return

    if client.mentioned_in(message):
        message.channel.send(get_joke)

    if re.match(dadPattern, message.content):
        message.channel.send(f'Hi {message.author.name}, I\'m Dadbot!')
        message.author.edit(nick=message.content[:32])

    if re.match(alphaPattern, message.content) \
       and message.content == message.content.upper():
        i = random.randint(0, len(loudMessages))
        msg = loudMessages[i].format(message.author.name)
        message.channel.send(msg)
