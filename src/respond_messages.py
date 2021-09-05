import random
import sys

import discord

from src import security
from src import dbHandler

responds = open("../rsc/responds.txt", 'r', encoding="utf8").read().split(";")
commands_list = open("../rsc/commands.txt", 'r', encoding="utf8").read().split(";")
bot_author = open('../private/author.txt', encoding="utf8").read()
bot_link = "https://github.com/KILLER04-star/Harald-Discord-Bot"
bot_error_link = "https://github.com/KILLER04-star/Harald-Discord-Bot/issues"
descriptions = open('../rsc/command_description.txt', 'r', encoding="utf8").read().split(";")


def z():
    file = open("../rsc/quotes.txt", 'r', encoding="utf8")
    messages = file.read().split(";")
    val = random.randint(0, len(messages) - 1)
    embed = discord.Embed(title=responds[53], colour=discord.Colour(0x3400ff),
                          url=bot_link, description=messages[val])
    embed.set_author(name=responds[26], url=bot_link)
    embed.set_footer(text=responds[29])

    return embed


def about():
    myid = '<@792004795703623691>'
    embed = discord.Embed(title=responds[33], colour=discord.Colour(0x32ff),
                          url=bot_link,
                          description=responds[12] + myid + responds[60])

    embed.set_author(name=responds[26], url=bot_link)
    embed.set_footer(text=responds[29])

    embed.add_field(name=responds[58], value=responds[59])
    embed.add_field(name=responds[56], value=responds[57])

    return embed


def help():
    embed = discord.Embed(title=responds[22], colour=discord.Colour(0xffffff),
                          url=bot_link,
                          description=responds[34])

    embed.set_author(name=responds[26], url=bot_link)
    embed.set_footer(text=responds[29])

    embed.add_field(name=commands_list[13], value=responds[63])
    embed.add_field(name=responds[30], value=commands_list[2])
    embed.add_field(name=responds[31], value=commands_list[1])
    embed.add_field(name=responds[32], value=commands_list[3])
    embed.add_field(name=responds[33], value=commands_list[11])

    return embed


def help_mittwoch():
    commands = commands_list
    embed = discord.Embed(title=responds[35], colour=discord.Colour(0xffffff),
                          url=bot_link, description=responds[36])

    embed.set_author(name=responds[26], url=bot_link)
    embed.set_footer(text=responds[29])

    embed.add_field(name=responds[37],
                    value=commands[7] + "\n" + responds[38])
    embed.add_field(name=responds[39],
                    value=commands[6] + "\n" + responds[40])
    embed.add_field(name=responds[41],
                    value=responds[42] + "\n" + responds[43] + commands[12])
    embed.add_field(name=responds[33], value=commands[11])
    return embed


def help_roulette():
    commands = commands_list
    embed = discord.Embed(title=responds[48], colour=discord.Colour(0xffffff),
                          url=bot_link,
                          description=responds[49])

    embed.set_author(name=responds[26], url=bot_link)
    embed.set_footer(text=responds[29])

    embed.add_field(name=responds[46],
                    value=commands[4] + "\n" + responds[50])
    embed.add_field(name=responds[33], value=commands[11])
    return embed


def help_koz():
    commands = commands_list
    embed = discord.Embed(title=responds[44], colour=discord.Colour(0xffffff),
                          url=bot_link,
                          description=responds[45])

    embed.set_author(name=responds[26], url=bot_link)
    embed.set_footer(text=responds[29])

    embed.add_field(name=responds[46], value=commands[10] + responds[47])
    embed.add_field(name=responds[33], value=commands[11])
    return embed


def show_commands():
    try:
        commands = commands_list

        index = 0
        embed = discord.Embed(title=responds[60], colour=discord.Colour(0xffffff),
                              url=bot_link,
                              description=responds[61])

        embed.set_author(name=responds[25], url=bot_link)
        embed.set_footer(text=responds[28])

        while index < 17:
            embed.insert_field_at(name=commands[index], value=descriptions[index], index=index)
            index += 1
        return embed
    except Exception as e:
        errorlog.logerror(e, "")


def ping(client):
    embed = discord.Embed(title=responds[75], color=discord.colour.Color.magenta(),
                          url=bot_link, description=responds[76])
    embed.add_field(name=responds[75], value=responds[77] + str(round((client.latency * 1000), 2)) + " ms.")
    embed.set_author(name=responds[26])
    embed.set_footer(text=responds[29])
    return embed


def kanal(message, conn, client):
    try:
        channel = dbHandler.get_channel_of_server(conn, message.guild.id, "Info")
        embed = discord.Embed(title=responds[54], colour=discord.Colour(0xf3ff00),
                              url=bot_link,
                              description=str(client.get_channel(channel)))

        embed.set_author(name=responds[26], url=bot_link)
        embed.set_footer(text=responds[29])
        return embed
    except Exception as e:

        embed = discord.Embed(title=responds[55], colour=discord.Colour(0xff0000),
                              url=bot_link, description=responds[14])

        embed.set_author(name=responds[26], url=bot_link)
        embed.set_footer(text=responds[29])

        embed.add_field(name=responds[22], value=responds[20])
        return embed


def set_channel(message, conn, bot_author):
    if security.isAdmin(message.author) or str(message.author) == bot_author:
        server_id = message.guild.id
        if dbHandler.server_already_existing(server_id, "Info", conn) == 0:  # Server is not in DB
            dbHandler.insert_data(str(server_id), str(message.channel.id), "Info", conn)
            embed = discord.Embed(title=responds[9], colour=discord.Colour(0xbd002),
                                  url=bot_link,
                                  description=responds[28])

            embed.set_author(name=responds[26], url=bot_link)
            embed.set_footer(text=responds[9])

            embed.add_field(name=responds[22], value=responds[20])
            return embed

        else:  # Server exists in DB
            try:
                #   globals()
                dbHandler.upgrade_channel(str(server_id), str(message.channel.id), "Info", conn)
                embed = discord.Embed(title=responds[27], colour=discord.Colour(0xbd002),
                                      url=bot_link,
                                      description=responds[28])

                embed.set_author(name=responds[26], url=bot_link)
                embed.set_footer(text=responds[29])

                embed.add_field(name=responds[22], value=responds[20])
                return embed
            except Exception as e:
                embed = discord.Embed(title=responds[25], colour=discord.Colour(0xd0021b),
                                      url=bot_error_link,
                                      description=responds[24])

                embed.set_author(name=responds[26], url=bot_link)
                embed.set_footer(text=responds[23])

                exc_type, exc_obj, exc_tb = sys.exc_info()
                error = str("Error_Code: " + str(e) + "\nError_Type: " + str(exc_type) + "\nLine: " + str(
                    exc_tb.tb_lineno) + "\n" + "Message: " + message.content.lower())

                embed.add_field(name=str(responds[21]), value=str(error))
                embed.add_field(name=responds[22], value=responds[20])

                return embed

    else:
        embed = discord.Embed(title=responds[67], colour=discord.Colour(0xd42500),
                              url=bot_link,
                              description=responds[68])

        embed.set_author(name=responds[26], url=bot_link)
        embed.set_footer(text=responds[29])

        embed.add_field(name=responds[69],
                        value=responds[70])
        embed.add_field(name=responds[71],
                        value=responds[72])
    return embed


def delkanal(message, conn):
    try:
        if security.isAdmin(message.author) or str(message.author == bot_author):
            dbHandler.delete_channel(str(message.guild.id), "Info", conn)
            embed = discord.Embed(title=responds[66], colour=discord.Colour(0xd432),
                                  url=bot_link,
                                  description=responds[73])

            embed.set_author(name=responds[26], url=bot_link)
            embed.set_footer(text=responds[29])

            return embed
        else:
            embed = discord.Embed(title=responds[67], colour=discord.Colour(0xd42500),
                                  url=bot_link,
                                  description=responds[68])

            embed.set_author(name=responds[26], url=bot_link)
            embed.set_footer(text=responds[29])

            embed.add_field(name=responds[69],
                            value=responds[70])
            embed.add_field(name=responds[71],
                            value=responds[72])

            return embed
    except Exception as e:
        embed = discord.Embed(title=responds[25], colour=discord.Colour(0xd0021b),
                              url=bot_error_link,
                              description=responds[24])

        embed.set_author(name=responds[26], url=bot_link)
        embed.set_footer(text=responds[23])

        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str("Error_Code: " + str(e) + "\nError_Type: " + str(exc_type) + "\nLine: " + str(
            exc_tb.tb_lineno) + "\n" + "Message: " + message.content.lower())

        embed.add_field(name=str(responds[21]), value=str(error))
        embed.add_field(name=responds[22], value=responds[20])

        errorlog.log_error(e, message.content.lower())

        return embed


def set_webhook(message, conn):
    if security.isAdmin(message.author) or str(message.author) == bot_author:
        server_id = message.guild.id
        if dbHandler.server_already_existing(server_id, "Webhook_Channels", conn):
            dbHandler.upgrade_channel(server_id, message.channel.id, "Webhook_Channels", conn)
        else:
            dbHandler.insert_data(server_id, message.channel.id, "Webhook_Channels", conn)
        embed = discord.Embed(title=responds[9], colour=discord.Colour(0x3ff54),
                              url=bot_link,
                              description=responds[74])

        embed.set_author(name=responds[26], url=bot_link)
        embed.set_footer(text=responds[29])

        return embed
    else:
        embed = discord.Embed(title=responds[67], colour=discord.Colour(0xd42500),
                              url=bot_link,
                              description=responds[68])

        embed.set_author(name=responds[26], url=bot_link)
        embed.set_footer(text=responds[29])

        embed.add_field(name=responds[69],
                        value=responds[70])
        embed.add_field(name=responds[71],
                        value=responds[72])

        return embed
def webhook(message, conn, client):
    try:
        channel = dbHandler.get_channel_of_server(conn, message.guild.id, "Webhook_Channels")
        embed = discord.Embed(title=responds[54], colour=discord.Colour(0xf3ff00),
                              url=bot_link,
                              description=str(client.get_channel(channel)))

        embed.set_author(name=responds[26], url=bot_link)
        embed.set_footer(text=responds[29])
        return embed
    except Exception as e:

        embed = discord.Embed(title=responds[55], colour=discord.Colour(0xff0000),
                              url=bot_link, description=responds[14])

        embed.set_author(name=responds[26], url=bot_link)
        embed.set_footer(text=responds[29])

        embed.add_field(name=responds[22], value=responds[20])
        return embed

def del_webhook(message,conn):
    try:
        if security.isAdmin(message.author) or str(message.author) == bot_author:
            dbHandler.delete_channel(str(message.guild.id), "Webhook_Channels", conn)
            embed = discord.Embed(title=responds[66], colour=discord.Colour(0xd432),
                                  url=bot_link,
                                  description=responds[73])

            embed.set_author(name=responds[26], url=bot_link)
            embed.set_footer(text=responds[29])

            return embed
        else:
            embed = discord.Embed(title=responds[67], colour=discord.Colour(0xd42500),
                                  url=bot_link,
                                  description=responds[68])

            embed.set_author(name=responds[26], url=bot_link)
            embed.set_footer(text=responds[29])

            embed.add_field(name=responds[69],
                            value=responds[70])
            embed.add_field(name=responds[71],
                            value=responds[72])

            return embed
    except Exception as e:
        embed = discord.Embed(title=responds[25], colour=discord.Colour(0xd0021b),
                              url=bot_error_link,
                              description=responds[24])

        embed.set_author(name=responds[26], url=bot_link)
        embed.set_footer(text=responds[23])

        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = str("Error_Code: " + str(e) + "\nError_Type: " + str(exc_type) + "\nLine: " + str(
            exc_tb.tb_lineno) + "\n" + "Message: " + message.content.lower())

        embed.add_field(name=str(responds[21]), value=str(error))
        embed.add_field(name=responds[22], value=responds[20])

        errorlog.log_error(e, message.content.lower())
        return embed