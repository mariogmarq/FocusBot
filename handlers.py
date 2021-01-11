import db
import discord
import time as t


async def time(message: discord.Message, DB: db.FocusDB, msg: []) -> None:
    if len(msg) == 1:
        await message.channel.send(
            "You have been focused for {} minutes!".format(DB.get_time(user_id=message.author.id) * 60))
    elif msg[1] == "-h":
        await message.channel.send("You have been focused for {} hours!".format(DB.get_time(user_id=message.author.id)))
    elif msg[1] == "-s":
        await message.channel.send(
            "You have been focused for {} seconds!".format(DB.get_time(user_id=message.author.id) * 3600))


async def start(message: discord.Message, user_time: dict) -> dict:
    if message.author.id in user_time.keys():
        await message.channel.send("You are already focusing!")
    else:
        user_time[message.author.id] = t.time()
        await message.channel.send("You have started to focus!")
    return user_time


async def end(message: discord.Message, user_time: dict, DB: db.FocusDB) -> dict:
    if message.author.id in user_time.keys():
        new_time = t.time() - user_time[message.author.id]
        hours = float(new_time) / 3600
        DB.update_time(user_id=message.author.id, time_added=hours)
        user_time.pop(message.author.id)
        await message.channel.send("You have stopped focusing!")
    else:
        await message.channel.send("You are not focusing!")

    return user_time


async def clear(message: discord.Message, DB: db.FocusDB) -> None:
    DB.update_time(user_id=message.author.id, time_added=-(DB.get_time(user_id=message.author.id)))
    await message.channel.send("Time cleared!")
