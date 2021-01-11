import discord
import os
import db
import time

client = discord.Client()
DB = db.FocusDB(file_name="db.db")
user_time = {}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global DB
    global user_time
    if message.author == client.user:
        return

    if message.content.startswith('$time'):
        await message.channel.send("You have been focused for {} minutes!".format(DB.get_time(user_id=message.author.id)*60))

    elif message.content.startswith('$start'):
        if message.author.id in user_time.keys():
            await message.channel.send("You are already focusing!")
        else:
            user_time[message.author.id] = time.time()
            await message.channel.send("You have started to focus!")

    elif message.content.startswith('$end'):
        if message.author.id in user_time.keys():
            new_time = time.time() - user_time[message.author.id]
            hours = float(new_time) / 3600
            DB.update_time(user_id=message.author.id, time_added=hours)
            await message.channel.send("You have stopped focusing!")
        else:
            await message.channel.send("You are not focusing!")

    elif message.content.startswith('$clear'):
        DB.update_time(user_id=message.author.id, time_added=-(DB.get_time(user_id=message.author.id)))
        await message.channel.send("Time cleared!")


client.run(os.getenv("TOKEN"))
