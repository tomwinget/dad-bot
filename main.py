#!/home/bots/.virtualenv/dadbot/bin/python3

import os
import re
import time
from datetime import datetime
import random
import requests
import logging
import discord
import traceback
import redis
import math


TOKEN = os.environ['dadToken']
vape_id = 436581339119222785
intents = discord.Intents.default()
intents.members = True
client = discord.Client(max_message=None, heartbeat_timeout=30, assume_unsync_clock=True, intents=intents)
r_local = redis.StrictRedis(decode_responses=True)


dadPattern = r"^(?:i’m|i'm|im|i am|imma) ?a? ([^\.\,\n]*)"
alphaPattern = r"^(\w+?\s+\w+?)+"
loudMessages = [
    'Now calm down {}!',
    'No yelling in the house {}!',
    'Lower your voice {}!',
    'You\'re being too loud {}!'
]
common_encoding = 'utf-8'
USERS_HASH = "USERS"
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
overlord = 147558756652154881

channel_topic = {
        'schoolhouse-rock': ['politic','trump','election','biden','president','dems','democrat','republican','cnn','fox']
        }

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
        elif "score" in str(message.content):
            num_dads = r_local.hget(USERS_HASH, message.author.id)
            logger.info("Telling %s they've been dadded %d times")
            await message.channel.send(f'Hey {message.author.mention}, you\'ve been dadded on {num_dads} times')
        elif "leaderboard" in str(message.content):
            all_mentions = message.mentions
            all_mentions.remove(client.user)
            if len(all_mentions) > 0:
                for i in range(len(all_mentions)):
                    user = all_mentions[i]
                    dad_count = r_local.hget(USERS_HASH, user.id)
                    if not dad_count:
                        dad_count = 0
                    logger.info("Sending dad for "+user.display_name)
                    await message.channel.send(f'{user.display_name} has been dadded on {dad_count} times')
            elif "total" in str(message.content):
                logger.info("Sending total dads")
                total_dads = r_local.hgetall(USERS_HASH)
                sorted_dads = sorted(total_dads.items(), key=lambda x: int(x[1]), reverse=True)
                logger.info("Sorted results: "+str(sorted_dads))
                leaderboard = '```\n --Top Dads: --\n'
                for index,user_id in enumerate(sorted_dads):
                    logger.info("getting user: "+str(user_id))
                    user = message.guild.get_member(int(user_id[0]))
                    count = user_id[1]
                    if user:
                        leaderboard += '#'+str(index+1)+'- '+str(user.name)+' with: '+str(count)+' dads\n'
                leaderboard += '```'
                await message.channel.send(leaderboard)
            else:
                logger.info("Sending top 5 dads")
                total_dads = r_local.hgetall(USERS_HASH)
                sorted_dads = sorted(total_dads.items(), key=lambda x: int(x[1]), reverse=True)
                logger.info("Sorted results: "+str(sorted_dads))
                leaderboard = '```\n --Top 5 Dads: --\n'
                for index,user_id in enumerate(sorted_dads[:5]):
                    logger.info("getting user: "+str(user_id))
                    logger.info("debug: "+str(user_id[0]))
                    logger.info("debug: "+str(user_id[1]))
                    user = message.guild.get_member(int(user_id[0]))
                    count = user_id[1]
                    if user:
                        leaderboard += '#'+str(index+1)+'- '+str(user.name)+' with: '+str(count)+' dads\n'
                leaderboard += '```'
                await message.channel.send(leaderboard)
        else:
            logger.info("joking with %s", str(message.author))
            await message.channel.send(get_joke())
    
    if "boomer" in str(message.content).lower():
        logger.info("boommering on %s", str(message.author))
        await message.channel.send("Hey that's our word!!")

    logger.info("Checking for dadding")
    groups = re.search(dadPattern, str(message.content), re.IGNORECASE)
    if groups:
        num_dads = ordinal(r_local.hincrby(USERS_HASH, message.author.id, 1))
        logger.info("dading on %s for the %d time", str(message.author), num_dads)
        if len(message.mentions) >= 1 and not message.reference:
            if message.author.id != overlord:
                await message.author.edit(nick=f'Totally not {message.mentions[0].display_name[:20]}')
                await message.channel.send(f'Hi totally not {message.author.mention}, I\'m Dadbot!')
            else:
                await message.channel.send(f'Hi totally not {message.mentions[0]}, I\'m Dadbot!')
            await message.channel.send(f'You\'ve been dadded for the {num_dads} time')
        else:
            if message.author.id != overlord:
                await message.author.edit(nick=groups.group(1)[:32])
                await message.channel.send(f'Hi {message.author.mention}, I\'m Dadbot!')
            else:
                await message.channel.send(f'Hi {groups.group(1)}, I\'m Dadbot!')
            await message.channel.send(f'You\'ve been dadded for the {num_dads} time')

    logger.info("Checking for yelling")
    if re.search(alphaPattern, str(message.content), re.IGNORECASE) \
       and str(message.content) == str(message.content).upper():
        logger.info("silencing %s", str(message.author))
        i = random.randint(0, len(loudMessages))
        msg = loudMessages[i-1].format(message.author.mention)
        await message.channel.send(msg)

    logger.info("Checking if this is the right channel")
    for channel, keywords in channel_topic.items():
        for keyword in keywords:
            if keyword in str(message.content).lower():
                chan = [chann for chann in message.guild.channels if chann.name.lower() == channel]
                logger.info("Found keyword: "+keyword+" and channels: "+str(chan))
                if chan and (channel not in message.channel.name):
                    logger.info("disabled")
                    # await message.channel.send('Hey {}, I think that belongs in {}'.format(message.author.mention, chan[0].mention))

    logger.info("done processing")
    return

@client.event
async def on_error(event, *args, **kwargs):
    message = args[0]
    logger.error(traceback.format_exc())
    logger.error("While processing message: "+str(message))
    message.channel.send('Boi howdy that last message was a thinker {}'.format(message.author.mention))

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
