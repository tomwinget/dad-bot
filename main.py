import os
import re
import random
import requests
import discord

TOKEN = os.environ['dadToken']
client = discord.Client()

dadPattern = r"^(?:i’m|i'm|im|i am) ?a? ([^\.\,\n]*)"
alphaPattern = r"^(\D+?\s+\D+?)+$"
loudMessages = [
    'Now calm down {}!',
    'No yelling in the house {}!',
    'Lower your voice {}!',
    'You\'re being too loud {}!'
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

    if client.user in message.mentions:
        await message.channel.send(get_joke())
    
    groups = re.match(dadPattern, message.content, re.IGNORECASE)
    if groups:
        await message.channel.send(f'Hi {groups.group(1)}, I\'m Dadbot!')
        await message.author.edit(nick=groups.group(1)[:32])

    if re.match(alphaPattern, message.content, re.IGNORECASE) \
       and message.content == message.content.upper():
        i = random.randint(0, len(loudMessages))
        msg = loudMessages[i-1].format(message.author.name)
        await message.channel.send(msg)

client.run(TOKEN)
