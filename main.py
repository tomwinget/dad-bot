#!/home/bots/.virtualenv/dadbot/bin/python3

import os
import re
import time
from datetime import datetime
import random
import requests
import logging
import discord


TOKEN = os.environ['dadToken']
vape_id = 436581339119222785
client = discord.Client(max_message=None, heartbeat_timeout=30, assume_unsync_clock=True)


dadPattern = r"^(?:i’m|i'm|im|i am) ?a? ([\w ]*)"
alphaPattern = r"^(\w+?\s+\w+?)+$"
loudMessages = [
    'Now calm down {}!',
    'No yelling in the house {}!',
    'Lower your voice {}!',
    'You\'re being too loud {}!'
]
common_encoding = 'utf-8'


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
        response.encoding = common_encoding
        return response.text
    else:
        return "Sorry I couldn't think of a joke right now :/"


@client.event
async def on_message(message):
    if message.author.bot:
        logger.info("got bot message")
        return

    if client.user in message.mentions:
        if "uptime" in str(message.content):
            timedelt = datetime.now() - start_time
            logger.info("Sharing uptime of %s", str(timedelt))
            await message.channel.send("I've been up for "+str(timedelt))
        else:
            logger.info("joking with %s", str(message.author))
            await message.channel.send(get_joke())
    
    if "boomer" in str(message.content).lower():
        logger.info("boommering on %s", str(message.author))
        await message.channel.send("Hey that's our word!!")


    logger.info("Checking for dadding")
    groups = re.search(dadPattern, str(message.content), re.IGNORECASE)
    if groups:
        logger.info("dading on %s", str(message.author))
        await message.channel.send(f'Hi {groups.group(1)}, I\'m Dadbot!')
        await message.author.edit(nick=groups.group(1)[:32])

    logger.info("Checking for yelling")
    if re.search(alphaPattern, str(message.content), re.IGNORECASE) \
       and str(message.content) == str(message.content).upper():
        logger.info("silencing %s", str(message.author))
        i = random.randint(0, len(loudMessages))
        if message.author.nick:
            msg = loudMessages[i-1].format(message.author.nick)
        else:
            msg = loudMessages[i-1].format(message.author.name)
        await message.channel.send(msg)

    logger.info("done processing")
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

logger.info("dad-bot starting")
start_time = datetime.now()
client.run(TOKEN)
logger.info("dad-bot stopped running")
