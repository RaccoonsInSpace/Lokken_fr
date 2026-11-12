### Vital for Bot
import discord
from discord import app_commands
from discord.ext import commands

import dotenv
import os

### fun
import matplotlib 
import random

### database
import sqlite3
import json 

### time leaderboard
import timeit

### reminders and timers
import time 
from discord.ext import tasks
from datetime import datetime
from zoneinfo import ZoneInfo

######## Settings

dotenv.load_dotenv()

all_guildes = False #False: only have slash commands for the test server, True: have slash commands for all servers, may take up to 1h to update

if not all_guildes:
    param_guild = discord.Object(id=os.getenv("DISCORD_GUILD_ID"))
else:
    param_guild = None  

######## Definitions and Parameters

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)

tree = app_commands.CommandTree(client)

######## When starting

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    #------------------------------------------------------------------------------
    channel_test = client.get_channel(1544691007977689098)
    await channel_test.send("I am now online!") # send starting message in test server channel

    channel_yap = client.get_channel(1552081358187274350)
    await channel_yap.send("I'm awake! :)")
    #------------------------------------------------------------------------------
    await tree.sync(guild=discord.Object(id=os.getenv("DISCORD_GUILD_ID")))
    print("Ready!") #sync slash command tree
    #------------------------------------------------------------------------------
    if not check_repeats.is_running():
            check_repeats.start()

@client.event
async def on_message(message):

    name = message.author.display_name
    number = random.randint(0,1000000)

    if number == 10:
        await message.channel.send(f"<@{message.author.id}> Congrats! You found the one in a million secret message! You get: nothing")         

    if message.author == client.user:
        return
    
    if message.content.lower().startswith('hello'):
        hello_number = random.randint(1,20)
        if hello_number == 4:
            await message.channel.send(f"Hello {name}")

    if message.content.startswith('test'):
            await message.channel.send('I am online!')
    
    if 'soen' in message.content:
            name = message.author.display_name
            await message.channel.send(f"HAHAHAHHA SOEN MENTIONED SO FUNNY AM I RIGHT HAHAH SO FUNNY HAHAHAHAHAHHAHAHAHAHHAHAHAHAHHAHAHAHAHAHHAHAHAH")

    if any(s in message.content.lower() for s in ('racoon', 'raccon', 'racon')):
         await message.channel.send("Uhm, it's spelled raccoon, actually :nerd: :point_up:")
    if 'raccoon' in message.content.lower():
         mommy_number = random.randint(1,20)
         if mommy_number == 4:
            await message.channel.send("Mommy? :pleading_face:")

    # if "bee" in message.content.lower():
    #      await message.channel.send("According to all known :speaking_head: laws :hammer: :writing_hand: of aviation :airplane:, there is no :x: way that a bee :bee: should be able :heavy_check_mark: to fly :butterfly: :bee: . Its wings :wind_blowing_face: are too small :white_small_square: to get its fat :busts_in_silhouette: little body :boy: off the ground :beach_umbrella: . The bee :bee: , of course, flies :wind_blowing_face: anyway. Because bees :bee: don’t :x: care :no_good: what humans :couple: think is impossible :no_entry_sign: .” SEQ. 75 - “INTRO TO BARRY” INT. BENSON HOUSE - DAY ANGLE ON: Sneakers :athletic_shoe: on the ground :earth_americas: :beach_umbrella: . Camera :movie_camera: PANS UP :arrow_up: to reveal :hushed: BARRY BENSON’S BEDROOM :bed: ANGLE ON: Barry’s hand :hand_splayed: flipping :middle_finger: through different sweaters :shirt: in his closet:closed_umbrella: . BARRY Yellow :yellow_heart: black :black_heart: , yellow :yellow_heart: black :black_heart: yellow :yellow_heart: black :black_heart: yellow :yellow_heart: black :black_heart: yellow :yellow_heart: black :black_heart:, yellow :yellow_heart: black :black_heart: ...oohh, black :black_heart: and yellow :yellow_heart:... ANGLE ON: Barry wearing the sweater :shirt: he picked :thinking: , looking :eyes: in the mirror . BARRY (CONT’D) Yeah :white_check_mark: , let’s shake :handshake: it up :arrow_up_small: a little :white_small_square: . He picks :eye: the black :black_heart: and yellow :yellow_heart: one :one: . He then goes :walking: to the sink :potable_water: , takes the top :top: off :mobile_phone_off: a CONTAINER :wastebasket: OF HONEY :honey_pot: , and puts some honey :honey_pot: into his hair :haircut: . He squirts :sweat_drops: some in his mouth :lips: and gargles :anger_right: . Then he takes :head_bandage: the lid :level_slider: off the bottle :champagne: , and rolls :newspaper2: some on like deodorant :snowflake: . CUT :scissors: TO :two: : INT. BENSON HOUSE :house: ")

    if client.user.mentioned_in(message):
        if any(s in message.content for s in ('thanks', 'thank', 'thx', 'ty')):
             await message.channel.send("No problem! :)")
        if any(s in message.content for s in ('ily', 'love', 'luv', 'ilysm')):
             await message.channel.send(f"I love you too {name}")
        if 'ping' in message.content:
             await message.channel.send("pong")
###############################################################################################################

######## Import all commands and stuff

### bot interactions with user etc
exec(open('main/commands/fun.py').read())

### store page 
exec(open('main/commands/shop.py').read())

### VC tracking etc 
exec(open('main/commands/tracking.py').read())

### reminders
exec(open('main/commands/reminders.py').read())

### test
exec(open('main/testing.py').read())


######## Start bot

client.run(os.getenv("SOCK_TOKEN"))

async def sleep():
     channel = 1561645954367496264
     await channel.send("Good night!")
     await client.close(os.getenv("DISCORD_TOKEN"))
