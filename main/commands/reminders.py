db = sqlite3.connect("shop.db")

def seconds_to_time(ts_epoch):
    time = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d %H:%M:%S')
    return time

def seconds_to_days(seconds):
    days = seconds // (24*60*60)
    hours = (seconds - days * 24*60*60) // (60*60)
    minutes = (seconds - days *24*60*60 - hours*60*60) // 60
    return (days, hours, minutes)

def number_to_bool(number):
    if number == 0:
        return (False, "No", "false", "off", "on its way")
    else:
        return (True, "Yes", "true", "on", "gone")

### Create database for reminders



#####################################################################################
#####################################################################################
#####################################################################################

cursor_shop.execute("""
    CREATE TABLE IF NOT EXISTS repeats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id INTEGER,
        user_id INTEGER,
        message TEXT,
        send_at INTEGER ,
        accountability BOOL DEFAULT 0,
        frequency INTEGER,
        random_range INTEGER DEFAULT 0,
        max_iteration INTEGER,
        iteration INTEGER DEFAULT 1,
        sent INTEGER DEFAULT 0
    )
""")

@tree.command(name="reminders", description="adds reminder, do /reminders_help for more info.", guild=param_guild)
async def reminder_add(interaction, message:str, hours:int, minutes:int, accountability:int=0, max_iteration:int=1, random_range:int=0):

    user_id = interaction.user.id

    frequency = abs(hours) * 60 * 60 + abs(minutes) * 60

    random_range_seconds = random_range 

    send_at = int(time.time()) + abs(random.randint(frequency - random_range_seconds , frequency + random_range_seconds))
    
    cursor_shop.execute(
            "INSERT INTO repeats (channel_id, user_id, message, send_at, accountability, frequency, max_iteration, random_range) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (interaction.channel.id, user_id, message, send_at, accountability, frequency, max_iteration, random_range_seconds)
    )
    db_shop.commit()

    await interaction.response.send_message(
        f"Alright, i will remind you to {message} every {hours} hours and {minutes} minutes +- {random_range} minutes {max_iteration} times."
        )


@tasks.loop(seconds=1)
async def check_repeats():
    now = int(time.time())

    repeats = db.execute(
        "SELECT id, channel_id, user_id, message, accountability, frequency, max_iteration, iteration, random_range FROM repeats "
        "WHERE send_at <= ? AND sent = 0",
        (now,)
    ).fetchall()


    for repeat_id, channel_id, user_id, message, accountability, frequency, max_iteration, iteration, random_range in repeats:
        channel = client.get_channel(channel_id)

        if channel is None:
            continue

        guild = channel.guild
        
        role = discord.utils.find(
            lambda r: "accountability" in r.name.lower(),
            guild.roles
        )

        if accountability == 0: 
            await channel.send(f"Hi <@{user_id}>, you asked me to remind you: {message}. Iteration: {iteration}")
        elif role is not None:
            await channel.send(f"WEE WOO WEE WOO! The user <@{user_id}> did not: {message}. <@&{role.id}>")
        else:
            await channel.send(f"WEE WOO WEE WOO! The user <@{user_id}> did not: {message}.")

        next_send = int(time.time()) + abs(random.randint(frequency - random_range, frequency + random_range))

        db.execute(
                        "UPDATE repeats SET send_at = ? WHERE id = ?",
                    (next_send, repeat_id)
                    )

        if max_iteration == 0:
            db.execute(
                            "UPDATE repeats SET iteration = ? WHERE id = ?",
                        (iteration + 1, repeat_id)
            )
        elif iteration < max_iteration:
            db.execute(
                "UPDATE repeats SET iteration = ? WHERE id = ?",
            (iteration + 1, repeat_id)
            )
        else:
            db.execute(
                "UPDATE repeats SET sent = 1 WHERE id = ?",
                (repeat_id,)
            )
            await channel.send(f"This was the last reminder")
        db.commit()


@check_repeats.before_loop
async def before_check_repeats():
    await client.wait_until_ready()

@tree.command(name="active_reminders", description="Shows all reminders that havent been sent yet", guild=param_guild)
async def view_reminders(interaction):
    embed=discord.Embed(title="Active repeat reminders", description="reminders", color=0xFF1C8E)

    cursor_shop.execute("""
    SELECT id
    FROM repeats
    WHERE sent = 0
""")

    reminders = [row[0] for row in cursor_shop.fetchall()]

    if not reminders:
        await interaction.response.send_message('Looks like theres no active reminders!')
    else: 
        for id in reminders:
            cursor_shop.execute(
                """
            SELECT channel_id, user_id, message, send_at, accountability, frequency, max_iteration, random_range
            FROM repeats
            WHERE id = ?
            """,
            (id,)
        )

            channel_id, user_id, message, send_at, accountability, frequency, max_iteration, random_range = cursor_shop.fetchone()

            user = await client.fetch_user(user_id)
            user_name = user.display_name

            embed.add_field(name=f"[id: {id}] Remind {user_name} to {message}", value=f"do /view_reminder {id} for more info", inline=False)

        await interaction.response.send_message(embed=embed)

@tree.command(name="view_reminder", description="Show specific reminder", guild=param_guild)
async def view_specific_reminder(interaction, id:int):

    embed=discord.Embed(title="Active repeat reminders", description="reminders", color=0xFF1C8E)

    cursor_shop.execute(
                """
            SELECT channel_id, user_id, message, send_at, accountability, frequency, iteration, max_iteration, random_range
            FROM repeats
            WHERE id = ?
            """,
            (id,)
    )

    channel_id, user_id, message, send_at, accountability, frequency, iteration, max_iteration, random_range = cursor_shop.fetchone()

    user = await client.fetch_user(user_id)

    embed.set_author(name=user.display_name, icon_url=user.avatar)

    embed.add_field(name=f"Remind {user.display_name} to {message}", value=f"in <#{channel_id}> at {seconds_to_time(send_at)}", inline=False)
    embed.add_field(name=f"Accountability", value=f"{number_to_bool(accountability)[1]}", inline=True)

    if max_iteration == 1:
        return
    else:
        embed.add_field(name=f"Send every {seconds_to_days(frequency)[1]} hours and {seconds_to_days(frequency)[2]} minutes +- {seconds_to_days(random_range)[1]} minutes", value=f"This is reminder {iteration} of {max_iteration}", inline=True)
    await interaction.response.send_message(embed=embed)

async def change_reminder(interaction, reminder_id:int, new_status:int):

    cursor_shop.execute(
                """
            SELECT user_id, message, send_at, sent
            FROM repeats
            WHERE id = ?
            """,
            (reminder_id,)
    )
    
    row = cursor_shop.fetchone()

    if row is None:
        await interaction.response.send_message(
            "There is no reminder with this ID."
        )
        return

    user_id, message, send_at, sent = row

    user = await client.fetch_user(user_id)

    user_name = user.display_name

    if sent == new_status:
        await interaction.response.send_message(f"This reminder is already {number_to_bool(new_status)[4]}")
        return 

    if interaction.user.guild_permissions.administrator:
        db.execute(
                    "UPDATE repeats SET sent = ? WHERE id = ?",
                    (new_status,reminder_id,)
        )

        db.commit()
    elif interaction.user.id != user_id:
        await interaction.response.send_message(f"This is not your reminder! It's rude to mess with other peoples reminders >:(")
        return
    else:
        db.execute(
                    "UPDATE repeats SET sent = ? WHERE id = ?",
                    (new_status,reminder_id,)
        )

        db.commit()

    await interaction.response.send_message(f"The reminder for {user_name} to {message} is now {number_to_bool(new_status)[4]}")

@tree.command(name="delete_reminder", description="Delete reminder. This can be undone! (I think?). Note: this deletes all iterations of a reminder", guild=param_guild)
async def delete_reminder(interaction, reminder_id:int):
    await change_reminder(interaction,reminder_id,1)
    

@tree.command(name="undelete_reminder", description="Undelete reminder. This can be undone! (I think?). Note: this undeletes all iterations of a reminder", guild=param_guild)
async def delete_reminder(interaction, reminder_id:int):
    await change_reminder(interaction,reminder_id,0)