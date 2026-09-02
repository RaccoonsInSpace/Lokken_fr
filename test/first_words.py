import discord
from discord import app_commands
from discord.ext import commands
import matplotlib

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)

tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(1544691007977689098)
    await channel.send('opened')
    await tree.sync(guild=discord.Object(id=1543919488188162110))
    print("Ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('test'):
        await message.channel.send('I am online!')

@tree.command(
    name="commandname",
    description="My first application Command",
    guild=discord.Object(id=1543919488188162110)
)
async def first_command(interaction):
    await interaction.response.send_message("Hello {0.display_name}!")
