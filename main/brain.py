### Vital for Bot
import discord
from discord import app_commands
from discord.ext import commands

import dotenv
import os

### fun
import matplotlib 
import random

### convinience 

from pathlib import Path #makes it so printing the module loaded things happens more automatically

######## Settings

dotenv.load_dotenv()

all_guildes = False #False: only have slash commands for the test server, True: have slash commands for all server, may take up to 1h to update

if not all_guildes:
    param_guild = discord.Object(id=os.getenv("DISCORD_GUILD_ID"))
else:
    param_guild = None  

######## Definitions and Parameters

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)

tree = app_commands.CommandTree(client)

######## When starting

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    #------------------------------------------------------------------------------
    channel = client.get_channel(1544691007977689098)
    await channel.send("I am now online!") # send starting message in test server channel
    #------------------------------------------------------------------------------
    await tree.sync(guild=discord.Object(id=1543919488188162110))
    print("Ready!") #sync slash command tree

###############################################################################################################

######## Import all commands and stuff

### test commands and stuff
exec(open('main/commands/fun.py').read())

### bot interactions with user etc
exec(open('main/testing.py').read())

### debugging
exec(open('main/debugging.py').read())




######## Start bot DO NOT SHARE THIS PART OF THE CODE WITH ANYONE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!















































client.run(os.getenv("DISCORD_TOKEN"))

