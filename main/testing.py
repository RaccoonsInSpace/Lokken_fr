user = "raccoons"
names = ["planet", "star", "moon", "sun", "galaxy"]
custom_id = "rac"
currencies = "planet:int=0, star:int=0, moon:int=0, sun:int=0, galaxy:int=0"
color = 0xFF5733


cursor_shop.execute(f"""
    CREATE TABLE IF NOT EXISTS {user}_rewards (
        rewards_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name STR
    )
""")

cursor_shop.execute(f"""
    CREATE TABLE IF NOT EXISTS {user}_quests (
        quests_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name STR
    )
""")

cursor_shop.execute(f"""
    CREATE TABLE IF NOT EXISTS {user}_inv (
        placeholder INT
    )
""")

cursor_shop.execute(f"""
    INSERT INTO {user}_inv (placeholder)
    SELECT 0
    WHERE NOT EXISTS (SELECT 1 FROM {user}_inv)
""")

db_shop.commit()

cursor_shop.execute(f"PRAGMA table_info({user}_rewards)")
columns = [row[1] for row in cursor_shop.fetchall()]

for currency in names:
    if currency not in columns:
        cursor_shop.execute(f"""
            ALTER TABLE {user}_rewards
            ADD {currency} INT DEFAULT 0;""")

        cursor_shop.execute(f"""
            ALTER TABLE {user}_quests
            ADD {currency} INT DEFAULT 0;""")

        cursor_shop.execute(f"""
            ALTER TABLE {user}_inv
            ADD {currency} INT DEFAULT 0;""")

db_shop.commit()

columns = ", ".join(names)
placeholders = ", ".join("?" for _ in names)

async def add(interaction, item:str, table:str, planet:int=0, star:int=0, moon:int=0, sun:int=0, galaxy:int=0):
        
        cursor_shop.execute(
            f"INSERT INTO {user}_{table} (name, {columns}) "
            f"VALUES (?, {placeholders})",
            (item, planet, star, moon, sun, galaxy)
        )

        db_shop.commit()

@tree.command(name=f"add_reward_{custom_id}", description="desc", guild=param_guild)
async def add_reward(interaction, item:str, planet:int=0, star:int=0, moon:int=0, sun:int=0, galaxy:int=0):
     await add(interaction,item,"rewards",planet, star, moon, sun, galaxy)

@tree.command(name=f"add_quest_{custom_id}", description="desc", guild=param_guild)
async def add_reward(interaction, item:str, table:str, planet:int=0, star:int=0, moon:int=0, sun:int=0, galaxy:int=0):
     await add(interaction,item,"quests",planet, star, moon, sun, galaxy)

def add_embed(embed, table, id):
            cursor_shop.execute(
                f"""
            SELECT name, {columns}
            FROM {user}_{table}
            WHERE {table}_id = ?
            """,
            (id,)
        )

            active_currencies = []
            check = 0

            item, *currency_values = cursor_shop.fetchone()

            for currency in currency_values:
                  if currency !=0:
                        active_currencies.append((names[check], currency))
                  check += 1
            price = []

            for currency in active_currencies:
                price.append(f":{currency[0]}: {currency[1]}")

            embed.add_field(name=f"{price} {item}", value=f"", inline=False)

async def show_table(interaction, table):
    embed=discord.Embed(title=f"{table}", description="", color=color)

    cursor_shop.execute(f"""
    SELECT {table}_id
    FROM {user}_{table}
""")

    items = [row[0] for row in cursor_shop.fetchall()]

    if not items:
        await interaction.response.send_message(f'Looks like there is no {table} yet')
    else: 
        for table_id in items:
            add_embed(embed, table, table_id)

        await interaction.response.send_message(embed=embed)

@tree.command(name=f"view_rewards_{custom_id}", description="test", guild=param_guild)
async def view_rewards(interaction):
     await show_table(interaction, "rewards")

@tree.command(name=f"view_quests_{custom_id}", description="test", guild=param_guild)
async def view_rewards(interaction):
     await show_table(interaction, "quests")

@tree.command(name=f"view_balance_{custom_id}", description="desc", guild=param_guild)
async def balance(interaction):
            embed=discord.Embed(title="Balance", description="", color=color)
            cursor_shop.execute(
                f"""
            SELECT {columns}
            FROM {user}_inv
            """,
        )

            active_currencies = []
            check = 0

            placeholder, *currency_values = cursor_shop.fetchone()

            for currency in currency_values:
                embed.add_field(name=f":{names[check]}: {currency}", value=f"", inline=False)
                check += 1

            await interaction.response.send_message(embed=embed)