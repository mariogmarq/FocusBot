import db
import discord
import time as t


async def time(message: discord.Message, DB: db.FocusDB, msg: list) -> None:
    if len(msg) == 1:
        await message.channel.send(
            "You have been focused for {} minutes!".format(int(DB.get_time(user_id=message.author.id) * 60)))
    elif len(message.mentions) != 0:
        await message.channel.send("{} has been focused for {} minutes!".format(message.mentions[0].mention,
                                                                                int(DB.get_time(
                                                                                    message.mentions[0].id) * 60)))
    elif msg[1] == "-h":
        await message.channel.send(
            "You have been focused for {} hours!".format(int(DB.get_time(user_id=message.author.id))))
    elif msg[1] == "-s":
        await message.channel.send(
            "You have been focused for {} seconds!".format(int(DB.get_time(user_id=message.author.id) * 3600)))


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


async def leader_board(message: discord.Message, client: discord.Client, DB: db.FocusDB) -> None:
    leaders = DB.leaders()
    to_say = ""
    for leader in leaders:
        user = await client.get_user(leader[0])
        to_say = to_say + "{} has been focused for {} minutes!\n".format(user.mention, leader[0] * 60)
    await message.channel.send(to_say)


async def max_strike(message: discord.Message, DB: db.FocusDB) -> None:
    strike = DB.get_max_strike(message.author.id)
    await message.channel.send("{} your max strike is {} minutes!".format(message.author.mention, int(strike * 60)))
