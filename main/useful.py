@tree.command(name="name", description="desc", guild=param_guild)
async def func(interaction):
    await interaction.response.send_message(number)

cursor_shop.execute("""
    CREATE TABLE IF NOT EXISTS name (
        something_id INT PRIMARY KEY,
    )
""")
db_shop.commit()

@tree.command(name="embedtest", description="test", guild=param_guild)
async def embed(interaction):
    embed=discord.Embed(title="Store", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)

    embed.add_field(name="[:star: 200] Super cool item yo", value="buy my stuff!!!", inline=False)

    await interaction.response.send_message(embed=embed)