



########################################################################################################

### create database etc
db_shop = sqlite3.connect("shop.db")
cursor_shop = db_shop.cursor()

########################################################################################################
######### SHOP #########################################################################################
########################################################################################################

### create shop table

cursor_shop.execute("""
    CREATE TABLE IF NOT EXISTS shop (
        item_id INT PRIMARY KEY,
        item TEXT,
        price INT,
        desc TEXT,
        is_role BOOL
    )
""")

db_shop.commit()

### Items

@tree.command(name="add_item", description="item id doesnt generate automatically, HAVE to give item UNIQUE id", guild=param_guild)
async def add_item(interaction, item_id:int, item_name:str, price:int, desc:str, is_role:bool=False):

    cursor_shop.execute("""
        SELECT item_id
        FROM shop
    """)
    
    item_ids = [row[0] for row in cursor_shop.fetchall()]
    
    if item_id in item_ids:
        await interaction.response.send_message("That item id is not unique! Choose another one")
    else: 
        cursor_shop.execute(
            """
            INSERT INTO shop
            (item_id, item, price, desc, is_role)
            VALUES (?, ?, ?, ?, ?)
            """,
            (item_id, item_name, price, desc, is_role)
        )

        db_shop.commit()

        await interaction.response.send_message(f"Added {item_name} to the shop")

@tree.command(name="delete_item", description="Delete items. This cannot be undone! (I think?)", guild=param_guild)
async def delete_item(interaction, item_id:int):
    item_delete = item_id

    cursor_shop.execute("""
            SELECT item
            FROM shop
            WHERE item_id = ?
            """,
            (item_id,)
        )
    
    item_delete_name = cursor_shop.fetchone()

    cursor_shop.execute(
        """
        DELETE FROM shop
        WHERE item_id = ?""",
        (item_delete,)
    )

    db_shop.commit()

    await interaction.response.send_message(f"Removed {item_delete_name} from the shop")
    return 

### Show store

@tree.command(name="shop", description="Buy stuff", guild=param_guild)
async def embed(interaction):
    embed=discord.Embed(title="Shop", description="shop", color=0xFF1C8E)

    cursor_shop.execute("""
    SELECT item_id
    FROM shop
""")

    items = [row[0] for row in cursor_shop.fetchall()]

    if not items:
        await interaction.response.send_message('Looks like theres nothing in the shop yet! Use /add_item to add items')
    else: 
        for item_id in items:
            cursor_shop.execute(
                """
            SELECT item, price, desc
            FROM shop
            WHERE item_id = ?
            """,
            (item_id,)
        )

            item, price, desc = cursor_shop.fetchone()

            embed.add_field(name=f"[:star: {price}] {item}", value=f"{desc}", inline=False)

        await interaction.response.send_message(embed=embed)


########################################################################################################
######### INVENTORY ####################################################################################
########################################################################################################

cursor_shop.execute("""
    CREATE TABLE IF NOT EXISTS user_inventory (
        user_id INTEGER PRIMARY KEY,
        stars INTEGER,
        planets INTEGER,
        items TEXT,
        pets TEXT
    )
""")

db_shop.commit()

@tree.command(name="join", description="join the adventure! (if you havent already)", guild=param_guild)
async def join(interaction):

    user_id = interaction.user.id

    cursor_shop.execute("""
            SELECT user_id
            FROM user_inventory
        """)
        
    user_ids = [row[0] for row in cursor_shop.fetchall()]

    if user_id in user_ids:
        await interaction.response.send_message("Youve already joined the adventure!")
    else:

        items = []
        items_json = json.dumps(items)
        
        cursor_shop.execute(
                    """
                    INSERT INTO user_inventory
                    (user_id, stars, planets, items)
                    VALUES (?, ?, ?, ?)
                    """,
                    (user_id, 0, 0, items_json)
                )
        db_shop.commit()
        await interaction.response.send_message("You successfully joined the adventure!")


@tree.command(name="view_inv", description="desc", guild=param_guild)
async def view_inv(interaction):
    user = interaction.user.id

    cursor_shop.execute("""
                SELECT user_id
                FROM user_inventory
            """)

    user_ids = [row[0] for row in cursor_shop.fetchall()]

    print(user_ids)
    
    if user not in user_ids:
        await interaction.response.send_message("You havent joined the adventure yet! /join to join the adventure")
        return 

    cursor_shop.execute("""
    SELECT stars, planets, items, pets
    FROM user_inventory
    WHERE user_id = ?
    """,
    (user,))

    stars, planets, items, pets = cursor_shop.fetchone()

    embed=discord.Embed(title="Inventory", description="", color=0xFF5733)

    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar)

    embed.add_field(name="Balance", value="", inline=False)
    embed.add_field(name="", value=f":star: {stars}", inline=False)
    embed.add_field(name="", value=f":ringed_planet: {planets}", inline=False)
    
    await interaction.response.send_message(embed=embed)


@tree.command(name="buy", description="buy items from the shop", guild=param_guild)
async def buy_item(interaction, item_id:str, amount:int):

    user = interaction.user.id
    
    cursor_shop.execute("""
            SELECT user_id
            FROM user_inventory
    """)
    
    user_ids = [row[0] for row in cursor_shop.fetchall()]

    if user not in user_ids:
        await interaction.response.send_message("You havent joined the adventure yet! /join to join the adventure")
        return 

    cursor_shop.execute(
                    """
                SELECT item, price, desc
                FROM shop
                WHERE item_id = ?
                """,
                (item_id)
            )

    item, price, desc = cursor_shop.fetchone()

    await interaction.response.send_message("You bought something! It falls out of your pockets because they have holes in them...")


print(f'Module \'shop\' loaded')