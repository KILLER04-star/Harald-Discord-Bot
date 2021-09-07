import random
import errorlog

import discord

responds = open("../rsc/responds.txt", 'r', encoding="utf8").read().split(";")
bot_link = "https://github.com/KILLER04-star/Harald-Discord-Bot"


async def roulette(message):
    bid = message.content.split('!')[1]

    if bid.lower() == "s":
        bid_param = -1

    elif bid.lower() == "r":
        bid_param = -2

    else:
        try:
            bid_param = int(bid)
            if bid_param < 0 or bid_param > 36:
                bid_param = 0
        except Exception as e:
            bid_param = -3
            errorlog.log_error(e)

    if bid_param == -3:
        await message.channel.send(str(responds[4]))
        return
    result = random.randint(0, 36)

    if bid_param == -1:
        won = result % 2 == 0 and not result == 0

    elif bid_param == -2:
        won = result % 2 == 1

    else:
        won = result == bid_param

    if won:
        embed = discord.Embed(title=responds[51], colour=discord.Colour(0x50e3c2),
                              url=bot_link,
                              description=responds[52])

        embed.set_author(name=responds[26], url=bot_link)
        embed.set_footer(text=responds[29])

        await message.channel.send(embed=embed)

    else:
        await message.channel.send(file=discord.File('../rsc/gestern.jpg'))


async def koz(message):
    bid = int(message.content.lower().split("!")[1])
    if bid < 0 or bid > 1:
        bid = 0
    result = random.randint(0, 1)

    if str(bid) == str(result):
        embed = discord.Embed(title=responds[51], colour=discord.Colour(0x50e3c2),
                              url=bot_link,
                              description=responds[52])

        embed.set_author(name=responds[26], url=bot_link)
        embed.set_footer(text=responds[29])
        await message.channel.send(embed=embed)
    else:
        await message.channel.send(file=discord.File('../rsc/gestern.jpg'))
