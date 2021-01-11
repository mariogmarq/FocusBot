import discord
import os
import db


client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


db = db.FocusDB(file_name="db.db")
print(db.get_time(1))

client.run(os.getenv("TOKEN"))