@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        name = message.author
        await message.channel.send(f"Hello {name}")

@tree.command(name="parrot", description="repeats whatever you say", guild=param_guild)
async def parrot(interaction, echo:str):
    await interaction.response.send_message(echo)


@tree.command(name="adding", description="adds two numbers", guild=param_guild)
async def adding(interaction, param1:int, param2:int):
    result = param1 + param2
    await interaction.response.send_message(result)

@tree.command(name="gambling", description="pick a number between 1 and 10", guild=param_guild)
async def gambling(interaction,guess:int):
    number = random.randint(0,10)
    if guess > 11:
        await interaction.response.send_message("oh-oh! Your guess is too large! Choose a number between 1 and 10")
    if guess < 1:
        await interaction.response.send_message("oh-oh! Your guess is too small! Choose a number between 1 and 10")
    elif guess != number:
        await interaction.response.send_message(f"oh no! That was wrong. The numbe was {number}")
    else:
        await interaction.response.send_message("That's correct! You get: nothing because Raccoons hasnt implemented a currency system yet")

print(f'Module \'fun\' loaded')
