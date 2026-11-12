print('ghi')

###########################################################################################
#########old reminder sys. non repeat

cursor_shop.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        send_at INTEGER NOT NULL,
        sent INTEGER NOT NULL DEFAULT 0,
        accountability INTEGER NOT NULL DEFAULT 0
    )
""")

db_shop.commit()

##############################################

@tree.command(name="reminder", description="reminds you, accurate up to 10 seconds", guild=param_guild)
async def reminder(interaction, message:str='default', seconds:int=0, minutes:int=0, hours:int=0, days:int=0, accountability:int=0):

    # if seconds or minutes or hours or days < 0:
    #     await interaction.response.send_message(f"I cant travel back in time, silly")

    secs = abs(seconds) + abs(minutes) * 60 + abs(hours) * 60 * 60 + abs(days) * 60 * 60 * 24 

    send_at = int(time.time()) + secs 

    user_id = interaction.user.id

    cursor_shop.execute(
            "INSERT INTO reminders (channel_id, user_id, message, send_at, accountability) VALUES (?, ?, ?, ?, ?)",
            (interaction.channel.id, user_id, message, send_at, accountability)
    )
    db_shop.commit()

    main_unit = days
    main_unit_text = "days"

    if days == 0:
        main_unit = hours
        main_unit_text = "hours"
    if hours == 0:
        main_unit = minutes
        main_unit_text = "minutes"
    if minutes == 0:
        main_unit = seconds
        main_unit_text = "seconds"

    await interaction.response.send_message(f"Alright, in {main_unit} {main_unit_text}, i will remind you to {message}")



@tasks.loop(seconds=1)
async def check_schedules():
    now = int(time.time())

    reminders = db.execute(
        "SELECT id, channel_id, user_id, message, accountability FROM reminders "
        "WHERE send_at <= ? AND sent = 0",
        (now,)
    ).fetchall()


    for schedule_id, channel_id, user_id, message, accountability in reminders:
        channel = client.get_channel(channel_id)

        if channel is None:
            continue

        guild = channel.guild
        
        role = discord.utils.find(
            lambda r: "accountability" in r.name.lower(),
            guild.roles
        )

        if accountability == 0: 
            await channel.send(f"Hi <@{user_id}>, you asked me to remind you: {message}")
        elif role is not None:
            await channel.send(f"WEE WOO WEE WOO! The user <@{user_id}> did not: {message}. <@&{role.id}>")
        else:
            await channel.send(f"WEE WOO WEE WOO! The user <@{user_id}> did not: {message}.")

        db.execute(
            "UPDATE reminders SET sent = 1 WHERE id = ?",
            (schedule_id,)
        )
        db.commit()


@check_schedules.before_loop
async def before_check_schedules():
    await client.wait_until_ready()

@tree.command(name="active_reminders", description="Shows all reminders that havent been sent yet", guild=param_guild)
async def view_reminders(interaction):
    embed=discord.Embed(title="Active reminders", description="shop", color=0xFF1C8E)

    cursor_shop.execute("""
    SELECT id
    FROM reminders
    WHERE sent = 0
""")

    reminders = [row[0] for row in cursor_shop.fetchall()]

    if not reminders:
        await interaction.response.send_message('Looks like theres no active reminders!')
    else: 
        for id in reminders:
            cursor_shop.execute(
                """
            SELECT channel_id, user_id, message, send_at, accountability
            FROM reminders
            WHERE id = ?
            """,
            (id,)
        )

            channel_id, user_id, message, send_at, accountability = cursor_shop.fetchone()

            user = await client.fetch_user(user_id)
            user_name = user.display_name

            embed.add_field(name=f"{id}) Remind {user_name} to {message}", value=f"send to <#{channel_id}> at {seconds_to_time(send_at)}. Accountability {accountability}", inline=False)

        await interaction.response.send_message(embed=embed)




@tree.command(name="reward_shop_start", description="desc", guild=param_guild)
async def func(interaction):

    user_id = interaction.user.id


    cursor_shop.execute(f"""
        CREATE TABLE IF NOT EXISTS reward_shop_{user_id} (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            item TEXT,
            description TEXT
        )
    """)

    cursor_shop.execute(f"""
        CREATE TABLE IF NOT EXISTS reward_quests_{user_id} (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            item TEXT,
            description TEXT
        )
    """)

    cursor_shop.execute(f"""
        CREATE TABLE IF NOT EXISTS reward_inv_{user_id} (
            currency STR,
            amt INT,
            desc STR
        )
    """)

    db_shop.commit()

    await interaction.response.send_message("done?")

@tree.command(name="add_currency", description="desc", guild=param_guild)
async def func(interaction, emoji:str, desc:str):

        user_id = interaction.user.id

        cursor_shop.execute(f"""
        ALTER TABLE reward_shop_{user_id}
        ADD {emoji} STR DEFAULT 0;""")

        cursor_shop.execute(f"""
        ALTER TABLE reward_quests_{user_id}
        ADD {emoji} STR DEFAULT 0;""")

        cursor_shop.execute(
            f"""
            INSERT INTO reward_inv_{user_id}
            (currency, amt, desc)
            VALUES (?, 0, ?)
            """,
            (emoji,desc)
        )

        db_shop.commit()

        await interaction.response.send_message("worked?")

@tree.command(name="add_reward", description="desc", guild=param_guild)
async def add_item(interaction, item_name:str, desc:str):

        user_id = interaction.user.id

        cursor_shop.execute(f"""
        SELECT currency
        FROM  reward_inv_{user_id}
    """)
    
        currencies = [row[0] for row in cursor_shop.fetchall()]

        cursor_shop.execute(
            f"""
            INSERT INTO reward_shop_{user_id}
            (item, desc)
            VALUES (?, ?)
            """,
            (item_name, desc)
        )

        db_shop.commit()

        channel = interaction-channel.id
        message = await channel.send("What currency would you like to use here?")

        for emoji in emojis:
            await message.add_reaction(emoji)

        