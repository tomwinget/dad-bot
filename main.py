#!/home/bots/.virtualenv/dadbot/bin/python3

import os
import re
import time
import random
import requests
import logging
import discord


TOKEN = os.environ['dadToken']
vape_id = 436581339119222785
client = discord.Client(max_message=None, heartbeat_timeout=120, assume_unsync_clock=True)


dadPattern = r"^(?:i’m|i'm|im|i am) ?a? ([^\.\,\n]*)"
alphaPattern = r"^(\D+?\s+\D+?)+$"
loudMessages = [
    'Now calm down {}!',
    'No yelling in the house {}!',
    'Lower your voice {}!',
    'You\'re being too loud {}!'
]


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


def get_joke():
    '''Makes request to dadjoke service and returns a formatted joke string
    '''
    response = requests.get(
        'https://icanhazdadjoke.com/',
        headers={
            'Accept': 'text/plain',
            'User-Agent': 'dad-bot (github.com/tomwinget/dad-bot)',
            'Connection': 'close'
        },timeout=5
    )
    if response:
        response.encoding = 'utf-8'
        return response.text
    else:
        return "Sorry I couldn't think of a joke right now :/"


@client.event
async def on_message(message):
    if message.author.bot:
        logger.info("got bot message")
        return

    if client.user in message.mentions:
        logger.info("joking with %s", str(message.author))
        await message.channel.send(get_joke())
    
    if "boomer" in str(message.content).lower():
        logger.info("boommering on %s", str(message.author))
        await message.channel.send("Hey that's our word!!")
    
    groups = re.match(dadPattern, message.content, re.IGNORECASE)
    if groups:
        logger.info("dading on %s", str(message.author))
        await message.channel.send(f'Hi {groups.group(1)}, I\'m Dadbot!')
        await message.author.edit(nick=groups.group(1)[:32])

    if re.match(alphaPattern, message.content, re.IGNORECASE) \
       and message.content == message.content.upper():
        logger.info("silencing %s", str(message.author))
        i = random.randint(0, len(loudMessages))
        if message.author.nick:
            msg = loudMessages[i-1].format(message.author.nick)
        else:
            msg = loudMessages[i-1].format(message.author.name)
        await message.channel.send(msg)

    return

@client.event
async def on_ready():
    logger.info("dad-bot reporting for duty")

@client.event
async def on_disconnect():
    logger.warning("dad-bot disconnecting")

@client.event
async def on_resumed():
    logger.warning("dad-bot resuming")

while True:
    try:
        logger.info("dad-bot starting")
        client.loop.run_until_complete(client.start(TOKEN))
        logger.info("dad-bot stopped running")
    except BaseException:
        time.sleep(5)

