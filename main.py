import discord
import os
import db
import handlers

client = discord.Client()
DB = db.FocusDB(file_name="db.db")
user_time = {}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("tracking your focus"))


@client.event
async def on_message(message):
    global DB
    global user_time
    if message.author == client.user:
        return

    #Parses message
    msg = message.content.split()

    #Responses
    if msg[0] == '$time':
        await handlers.time(message, DB, msg)

    elif msg[0] == '$start':
        user_time = await handlers.start(message, user_time)

    elif msg[0] == '$end':
        user_time = await handlers.end(message, user_time, DB)

    elif msg[0] == '$clear':
        await handlers.clear(message, DB)

    elif msg[0] == '$leaders':
        await handlers.leader_board(message, client, DB)

    elif msg[0] == '$strike':
        await handlers.max_strike(message, DB)


client.run(os.getenv("TOKEN"))
