import asyncio

import discord
import random
import sqlite3

import datetime

from sqlite3 import Error

import base64
import sys

import praw
from discord.ext import commands
import configparser
global reddit
global reddit_clientid
global reddit_clientSecret
global reddit_useragent

global discord_token

global bot_link
bot_link = "https://github.com/KILLER04-star/Harald-Discord-Bot"
global bot_error_link
bot_error_link = "https://github.com/KILLER04-star/Harald-Discord-Bot/issues"
global bot_author_link
bot_author_link = "https://github.com/KILLER04-star"


class MyClient(discord.Client):
    # Login
    config = configparser.ConfigParser()
    config.read('../private/praw.ini')

    global keys
    keys = open("../private/keys.txt", 'r', encoding="utf8").read().split(";")
    global discord_token
    discord_token = keys[0]
    global bot
    bot = commands.Bot(command_prefix="$")
    global bot_author
    bot_author = open('../private/author.txt',encoding="utf8").read()
    global commands_list
    commands_list = open("../rsc/commands.txt", 'r', encoding="utf8").read().split(";")
    global responds
    responds = open("../rsc/responds.txt", 'r', encoding="utf8").read().split(";")
    global sent_available
    sent_available = True
    global trigger_day
    global webhook_counter
    webhook_counter = 0
    global isWednesday
    isWednesday = False

    global reddit
    reddit = praw.Reddit(client_id=config.get('praw', 'reddit_client_id'), client_secret=config.get('praw','reddit_client_secret'),
                         user_agent=config.get('praw', 'reddit_user_agent'))
    global sub

    global subs
    subs = []

    async def on_ready(self):
        print("Ich habe mich eingeloggt. Beep Bop.")

        global auto_delete
        auto_delete = False
        global conn
        conn = self.create_connection(r'../private/info.db')
        self.create_tables(conn)
        global responds
        global trigger_day
        trigger_day = 3
        print("The bot will be triggered on the " + str(trigger_day) + ". day of the week.")
        await MyClient.change_presence(self, activity=discord.Game(name=responds[64]))
        await asyncio.gather(self.check_date())

    # On_Message_Received
    async def on_message(self, message):
        try:
            global conn
            global commands_list
            global responds
            global descriptions


            descriptions = open("../rsc/command_description.txt", 'r', encoding="utf8").read().split(";")
            commands = commands_list

            if message.author == client.user:
                return
            if message.author.bot:
                return

            if message.content.lower() == commands[0]:
                embed = discord.Embed(title=responds[22], colour=discord.Colour(0xffffff),
                                      url=bot_link,
                                      description=responds[34])

                embed.set_author(name=responds[26], url=bot_link)
                embed.set_footer(text=responds[29])

                embed.add_field(name=commands[13], value=responds[63])
                embed.add_field(name=responds[30], value=commands[2])
                embed.add_field(name=responds[31], value=commands[1])
                embed.add_field(name=responds[32], value=commands[3])
                embed.add_field(name=responds[33], value=commands[11])
                await message.channel.send(embed=embed)

            if message.content.lower().startswith("$help -mittwoch"):
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
                await message.channel.send(embed=embed)

            if message.content.lower().startswith("$help -roulette"):
                embed = discord.Embed(title=responds[48], colour=discord.Colour(0xffffff),
                                      url=bot_link,
                                      description=responds[49])

                embed.set_author(name=responds[26], url=bot_link)
                embed.set_footer(text=responds[29])

                embed.add_field(name=responds[46],
                                value=commands[4] + "\n" + responds[50])
                embed.add_field(name=responds[33], value=commands[11])
                await message.channel.send(embed=embed)

            if message.content.lower().startswith("$help -koz"):
                embed = discord.Embed(title=responds[44], colour=discord.Colour(0xffffff),
                                      url=bot_link,
                                      description=responds[45])

                embed.set_author(name=responds[26], url=bot_link)
                embed.set_footer(text=responds[29])

                embed.add_field(name=responds[46], value=commands[9] + responds[47])
                embed.add_field(name=responds[33], value=commands[10])
                await message.channel.send(embed=embed)

            if message.content.startswith("$roulette"):
                bid = message.content.split('!')[1]

                bid_param = -3

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
                        self.log_error(e)

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

            elif message.content.lower().startswith("$private hilfe"):
                await message.author.send(str(responds[6]))

            elif message.content.lower().startswith("$bot -mittwoch -fire"):
                if self.isAdmin(message.author) or str(message.author == bot_author):
                    await message.channel.send(message.guild.roles[0], file=discord.File('../rsc/mittwoch.png'))

            elif message.content.lower().startswith("$setzkanal"):
                if self.isAdmin(message.author) or str(message.author) == bot_author:
                    server_id = message.guild.id
                    if self.server_already_existing(server_id, "Info", conn) == 0:  # Server is not in DB
                        self.insert_data(str(server_id), str(message.channel.id), "Info", conn)
                        embed = discord.Embed(title=responds[9], colour=discord.Colour(0xbd002),
                                              url=bot_link,
                                              description=responds[28])

                        embed.set_author(name=responds[26], url=bot_link)
                        embed.set_footer(text=responds[9])

                        embed.add_field(name=responds[22], value=responds[20])
                        await message.channel.send(embed=embed)

                    else:  # Server exists in DB
                        try:
                            #   globals()
                            self.upgrade_channel(str(server_id), str(message.channel.id), "Info", conn)
                            embed = discord.Embed(title=responds[27], colour=discord.Colour(0xbd002),
                                                  url=bot_link,
                                                  description=responds[28])

                            embed.set_author(name=responds[26], url=bot_link)
                            embed.set_footer(text=responds[29])

                            embed.add_field(name=responds[22], value=responds[20])
                            await message.channel.send(embed=embed)
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

                            await message.channel.send(embed=embed)
                            self.log_error(e, message.content.lower())

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

                    await message.channel.send(
                        embed=embed)


            elif message.content.lower().startswith("$z"):
                file = open("../rsc/quotes.txt", 'r', encoding="utf8")
                messages = file.read().split(";")
                val = random.randint(0, len(messages) - 1)
                embed = discord.Embed(title=responds[53], colour=discord.Colour(0x3400ff),
                                      url=bot_link, description=messages[val])

                embed.set_author(name=responds[26], url=bot_link)
                embed.set_footer(text=responds[29])
                await message.channel.send(embed=embed)

            elif message.content.lower().startswith("$koz"):
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

            elif message.content.lower().startswith("$about"):
                myid = '<@792004795703623691>'
                embed = discord.Embed(title=responds[33], colour=discord.Colour(0x32ff),
                                      url=bot_link,
                                      description=responds[12] + myid + responds[60])

                embed.set_author(name=responds[26], url=bot_link)
                embed.set_footer(text=responds[29])

                embed.add_field(name=responds[58], value=responds[59])
                embed.add_field(name=responds[56], value=responds[57])

                await message.channel.send(embed=embed)

            elif message.content.lower().startswith("$kanal"):
                channel = self.get_channel_of_server(conn, message.guild.id, "Info")

                if channel is None:
                    embed = discord.Embed(title=responds[55], colour=discord.Colour(0xff0000),
                                          url=bot_link, description=responds[14])

                    embed.set_author(name=responds[26], url=bot_link)
                    embed.set_footer(text=responds[29])

                    embed.add_field(name=responds[22], value=responds[20])
                    await message.channel.send(str(responds[14]))
                else:
                    embed = discord.Embed(title=responds[54], colour=discord.Colour(0xf3ff00),
                                          url=bot_link,
                                          description=str(client.get_channel(channel)))

                    embed.set_author(name=responds[26], url=bot_link)
                    embed.set_footer(text=responds[29])
                    await message.channel.send(embed=embed)

            elif message.content.lower().startswith("$see_data") and bot_author == str(message.author):
                await self.send_meme()
            elif message.content.lower().startswith("$show_commands"):

                index = 0
                embed = discord.Embed(title=responds[61], colour=discord.Colour(0xffffff),
                                      url=bot_link,
                                      description=responds[62])

                embed.set_author(name=responds[26], url=bot_link)
                embed.set_footer(text=responds[29])

                while index < 18:
                    embed.insert_field_at(name=commands[index], value=descriptions[index], index=index)
                    index += 1
                await message.channel.send(embed=embed)

            elif message.content.lower().startswith("$delkanal"):
                try:
                    if self.isAdmin(message.author) or str(message.author == bot_author):
                        self.delete_channel(str(message.guild.id), "Info", conn)
                        embed = discord.Embed(title=responds[66], colour=discord.Colour(0xd432),
                                              url=bot_link,
                                              description=responds[73])

                        embed.set_author(name=responds[26], url=bot_link)
                        embed.set_footer(text=responds[29])

                        await message.channel.send(
                            embed=embed)
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

                        await message.channel.send(
                            embed=embed)
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

                    await message.channel.send(embed=embed)
                    self.log_error(e, message.content.lower())

            elif message.content.lower().startswith("$setz_webhook"):
                if self.isAdmin(message.author) or str(message.author) == bot_author:
                    server_id = message.guild.id
                    if self.server_already_existing(server_id, "Webhook_Channels", conn):
                        self.upgrade_channel(server_id, message.channel.id, "Webhook_Channels", conn)
                    else:
                        self.insert_data(server_id, message.channel.id, "Webhook_Channels", conn)
                    embed = discord.Embed(title=responds[9], colour=discord.Colour(0x3ff54),
                                          url=bot_link,
                                          description=responds[74])

                    embed.set_author(name=responds[26], url=bot_link)
                    embed.set_footer(text=responds[29])

                    await message.channel.send(embed=embed)
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

                    await message.channel.send(
                        embed=embed)
            elif message.content.lower().startswith("$webhook"):
                channel = self.get_channel_of_server(conn, message.guild.id, "Webhook_Channels")

                if channel is None:
                    embed = discord.Embed(title=responds[55], colour=discord.Colour(0xff0000),
                                          url=bot_link, description=responds[14])

                    embed.set_author(name=responds[26], url=bot_link)
                    embed.set_footer(text=responds[29])

                    embed.add_field(name=responds[22], value=responds[20])
                    await message.channel.send(str(responds[14]))
                else:
                    embed = discord.Embed(title=responds[54], colour=discord.Colour(0xf3ff00),
                                          url=bot_link,
                                          description=str(client.get_channel(channel)))

                    embed.set_author(name=responds[26], url=bot_link)
                    embed.set_footer(text=responds[29])
                    await message.channel.send(embed=embed)
            elif message.content.lower().startswith("$del_webhook"):
                try:
                    if self.isAdmin(message.author) or str(message.author) == bot_author:
                        self.delete_channel(str(message.guild.id), "Webhook_Channels", conn)
                        embed = discord.Embed(title=responds[66], colour=discord.Colour(0xd432),
                                              url=bot_link,
                                              description=responds[73])

                        embed.set_author(name=responds[26], url=bot_link)
                        embed.set_footer(text=responds[29])

                        await message.channel.send(
                            embed=embed)
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

                        await message.channel.send(
                            embed=embed)
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

                    await message.channel.send(embed=embed)
                    self.log_error(e, message.content.lower())
            elif message.content.lower().startswith("$ping"):
                embed = discord.Embed(title=responds[75], color=discord.colour.Color.magenta(),
                                      url=bot_link, description=responds[76])
                embed.add_field(name=responds[75], value=responds[77] + str(client.latency * 1000) + " ms.")
                embed.set_author(name=responds[26])
                embed.set_footer(text=responds[29])
                await message.channel.send(embed=embed)



        except Exception as e:
            embed = discord.Embed(title=responds[25], colour=discord.Colour(0xd0021b),
                                  url=bot_error_link,
                                  description=responds[24])

            embed.set_author(name=responds[26], url=bot_link)
            embed.set_footer(text=responds[23])

            exc_type, exc_obj, exc_tb = sys.exc_info()
            error = str("Error_Code: " + str(e) + "\nError_Type: " + str(exc_type) + "\nLine: " + str(
                exc_tb.tb_lineno))
            embed.add_field(name=str(responds[21]), value=str(error))
            embed.add_field(name=responds[22], value=responds[20])

            await message.channel.send(embed=embed)
            self.log_error(e, message.content.lower())

    async def on_guild_join(self, guild):
        global commands_list
        commands = commands_list
        global responds
        global descriptions
        descriptions = open("../rsc/command_description.txt", 'r', encoding="utf8").read().split(";")
        index = 0
        embed = discord.Embed(title=responds[61], colour=discord.Colour(0xffffff),
                              url=bot_link,
                              description=responds[62])

        embed.set_author(name=responds[26], url=bot_link)
        embed.set_footer(text=responds[29])

        while index < 13:
            embed.insert_field_at(name=commands[index], value=descriptions[index], index=index)
            index += 1
        await guild.text_channels[0].send(embed=embed)

    def create_connection(self, db_file):
        # opens a connection to a sqlite-database containing necessary
        # information about the servers, like in which channel the bot is supposed to send memes
        conn = None

        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
            return conn
        except Error as e:
            self.log_error(e, "")
        return conn

    def create_tables(self, conn):
        try:
            c = conn.cursor()

            c.execute('''CREATE TABLE Info (Server_id text, Channel_id text)''')
            c.execute('''CREATE TABLE Webhook_Channels (Server_id text, Channel_id text)''')
            c.execute('''CREATE TABLE Status(Server_id text, Sent text, Notes text)''')

            conn.commit()
        except Error as e:
            self.log_error(e, "")

    def insert_data(self, server_id, channel_id, table, conn):

        server_id = self.encode(server_id)
        channel_id = self.encode(channel_id)

        values = [server_id, channel_id]

        c = conn.cursor()

        c.execute('INSERT INTO ' + table + ' VALUES (?,?)', values)

        conn.commit()

    def server_already_existing(self, server_id, table, conn):
        c = conn.cursor()
        server_id = self.encode(server_id)
        server_id = (server_id,)
        c.execute('SELECT * FROM ' + table + ' WHERE Server_id=?', server_id)

        return len(c.fetchall())

    def upgrade_channel(self, Server_id, channel_id, table, conn):
        c = conn.cursor()
        const_server_id = Server_id
        Server_id = self.encode(Server_id)
        Server_id = (Server_id,)

        c.execute('DELETE FROM ' + table + ' WHERE Server_id=?', Server_id)

        conn.commit()

        self.insert_data(const_server_id, channel_id, table, conn)

    def delete_channel(self, server_id, table, conn):
        c = conn.cursor()
        my_server_id = self.encode(server_id)
        my_server_id = (my_server_id,)

        c.execute('DELETE FROM ' + table + ' WHERE Server_id=?', my_server_id)

        conn.commit()

        self.delete_server_status(server_id=server_id)
    def get_data(self, table):
        global conn

        c = conn.cursor()

        c.execute('SELECT * FROM ' + table)

        return c.fetchall()

    async def send_meme(self):
        success = False
        data = self.get_data("Info")

        notes = "none"

        server_id = 0

        index = 0
        try:
            for i in data:
                info = data[index]
                channel_id = int(self.decode(str(info).replace("'", "").split(",")[1].replace("(", "").replace(")", "")))
                channel = client.get_channel(channel_id)
                server_id = int(
                    str(self.decode(str(info).replace("'", "").split(",")[0].replace("(", "").replace(")", ""))))
                guild_role = client.get_guild(server_id).roles[0]
                if not self.get_server_status(server_id):
                    await channel.send(guild_role, file=discord.File('../rsc/mittwoch.png'))
                else:
                    print("Sent: "+str(self.get_server_status(server_id)))
                index += 1
                success = True
        except Exception as e:
            notes = str(e)
            self.log_error(e, "")

        self.update_server_status(server_id, success, notes)

    def update_server_status(self, server_id, status, notes):
        c = conn.cursor()
        const_server_id = server_id
        Server_id = self.encode(server_id)
        Server_id = (Server_id,)

        c.execute('DELETE FROM ' + 'Status' + ' WHERE Server_id=?', Server_id)

        conn.commit()

        self.set_server_status(const_server_id, status, notes)



    def delete_server_status(self, server_id):
        global conn
        c = conn.cursor()
        server_id = self.encode(server_id)
        server_id = (server_id,)

        c.execute('DELETE FROM Status WHERE Server_id=?', server_id)

        conn.commit()

    def get_server_status(self, server_id):
        global conn
        result = False
        c = conn.cursor()
        server_id = self.encode(server_id)
        server_id = (server_id,)

        c.execute('SELECT Sent FROM Status WHERE Server_id=?', server_id)
        try:
            result = bool(str((c.fetchone()).replace("[", "").replace("(", "").
                      replace("'", "").replace(",", "").replace(")", "").replace("]", "")))
        except Exception as e:
            self.log_error(e, "")
        return result

    def set_server_status(self, server_id, status, notes):
        global conn
        c = conn.cursor()

        server_id = self.encode(server_id)

        values = [server_id, status, notes]

        c.execute('INSERT INTO Status VALUES (?,?,?)', values)

        conn.commit()


    def get_sub_names(self):
        global conn

        c = conn.cursor()

        c.execute('SELECT Sub_Name FROM sub_names')

        return c.fetchall()

    async def webhook(self):
        data = self.get_data("Webhook_Channels")

        sub_names = self.get_sub_names()

        index = 0

        global isWednesday, sub
        try:
            if isWednesday:
                sub_names.append("ich_iel")
                sub_names.append("de")
            else:
                sub_names.remove("ich_iel")
                sub_names.remove("de")
        except Exception as e:
            self.log_error(e, "")

        for i in data:
            try:
                info = data[index]
                channel_id = int(
                    self.decode(str(info).replace("'", "").split(",")[1].replace("(", "").replace(")", "")))
                channel = client.get_channel(channel_id)

                index = 0

                while index < 27:
                    global reddit
                    subs.append(reddit.subreddit(str(sub_names[index]).replace("'", "").replace(",", "").replace("(", "").replace(")", "").replace(" ", "")))

                    sub = random.choice(subs)

                    index = index + 1

                top = sub.top(limit=1000)
                allsubs = []

                for submission in top:
                    allsubs.append(submission)

                randomsub = random.choice(allsubs)

                name = randomsub.title
                url = randomsub.url
                em = discord.Embed(
                    title=name,
                    color=discord.Color.blurple()
                )
                #  em.add_field(name="Beschreibung:", value=str(sub.description))
                em.set_footer(text="r/" + str(sub.display_name))
                em.set_image(url=url)
                await channel.send(embed=em)
                index += 1
            except Exception as e:
                self.log_error(e, "")


    def get_channel_of_server(self, conn, server_id, table):
        c = conn.cursor()
        server_id = self.encode(server_id)
        server_id = (server_id,)

        c.execute('SELECT Channel_id FROM ' + table + ' WHERE Server_id=?', server_id)
        result = (str(c.fetchall()).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("[",
                                                                                                                "").replace(
            "]", ""))
        result = int(self.decode(str(result)))
        return result

    def reset_server_status(self):
        server_ids = self.get_all_servers()

        for i in server_ids:
            self.update_server_status(i, "False", "Last_Updated: "+str(datetime.datetime.today()))

    def get_all_servers(self):
        global conn
        ids = []
        c = conn.cursor()
        c.execute('SELECT Server_id FROM Info')
        server_id = self.decode(str(c.fetchall()).replace("[","").replace("]","").replace("'","").replace("(","").replace(")","").replace(",",""))
        ids.append(server_id)
        return ids

    async def check_date(self):
        global sent_available
        day = (datetime.datetime.today().weekday())
        minute = datetime.datetime.today().minute
        global trigger_day
        global isWednesday
        if str(day) == str(int(int(trigger_day) - 1)) and sent_available:
            isWednesday = True
            await self.send_meme()
            sent_available = False
        elif str(day) != str(int(int(trigger_day) - 1)):
            isWednesday = False
            sent_available = True
            self.reset_server_status()
         #   self.get_all_channels()

        if minute % 50 == 0 and minute > 0:
            index = 0
            while index <= 3:
                index = index + 1
                await self.webhook()
        #   await self.wait()
        await asyncio.sleep(15)
        await asyncio.gather(self.check_date())

    def isAdmin(self, user):
        return str(user.guild_permissions) == "<Permissions value=2147483647>"

    def encode(self, text):
        bytes = base64.b64encode(str(text).encode("utf-8"))
        return str(bytes, "utf-8")

    def decode(self, text):
        bytes = base64.b64decode(str(text).encode("utf-8"))
        return str(bytes, "utf-8")

    def log_error(self, exception, message):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        message = str("Error_Code: " + str(exception) + "\nError_Type: " + str(exc_type) + "\nLine: " + str(exc_tb.tb_lineno) + "\nMessage: "+str(message))
        file = open("../log/errorlog.txt", "a+", encoding="utf-8")
        file.write('\n' + "-------------------------------" + '\n')
        file.write(str(datetime.datetime.today()) + " " + message)
        file.close()
        print(str(datetime.datetime.today()) + " " + message)

client = MyClient()
client.run(discord_token)  # Manuell das Token einf??gen | vor jedem Commit und Jedem Push unbedingt entfernen!