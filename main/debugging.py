
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('test'):
        await message.channel.send('I am online!')



print(f'Module \'debugging\' loaded')
