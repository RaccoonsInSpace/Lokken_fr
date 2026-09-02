
@tree.command(name="formattest", description="test", guild=param_guild)
async def adding(interaction):
    await interaction.response.send_message("this is a normal message \n" \
    "# this is a header \n" \
    "```this is a code block```\n " \
    "**this is bold**\n")

@tree.command(name="embedtest", description="test", guild=param_guild)
async def embed(interaction):
    embed=discord.Embed(title="Store", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)

    embed.add_field(name="[:star: 200] Super cool item yo", value="buy my stuff!!!", inline=False)

    await interaction.response.send_message(embed=embed)



print(f'Module \'testing\' loaded')
