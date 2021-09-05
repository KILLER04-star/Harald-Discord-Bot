import asyncio
import base64
# from discord_slash.utils.manage_commands import create_option
import configparser
import datetime
import random
import sqlite3
import sys
import time
from sqlite3 import Error

import discord
import errorlog
from src import games
from src import respond_messages
from src import security
from src import dbHandler
import praw
from discord.ext import commands
from discord_slash import SlashCommand

global reddit
global reddit_clientid
global reddit_clientSecret
global reddit_useragent

global discord_token

from discord import client

global bot_link
bot_link = "https://github.com/KILLER04-star/Harald-Discord-Bot"
global bot_error_link
bot_error_link = "https://github.com/KILLER04-star/Harald-Discord-Bot/issues"
global bot_author_link
bot_author_link = "https://github.com/KILLER04-star"

global sending_meme
sending_meme = False

global Games


class MyClient(discord.Client):
    # Login
    config = configparser.ConfigParser()
    config.read('../private/praw.ini')

    global keys
    keys = open("../private/keys.txt", 'r', encoding="utf8").read().split(";")
    global discord_token
    discord_token = keys[0]
    global bot
    bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())
    slash = SlashCommand(bot)
    global bot_author
    bot_author = open('../private/author.txt', encoding="utf8").read()
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

    global context

    global reddit
    reddit = praw.Reddit(client_id=config.get('praw', 'reddit_client_id'),
                         client_secret=config.get('praw', 'reddit_client_secret'),
                         user_agent=config.get('praw', 'reddit_user_agent'))
    global sub

    global subs
    subs = []
    global sub_data

    async def on_ready(self):
        print("Ich habe mich eingeloggt. Beep Bop.")

        global conn
        conn = dbHandler.create_connection(r'../private/info.db')
        dbHandler.create_tables(conn)
        global responds
        global trigger_day
        trigger_day = 3
        print("The bot will be triggered on the " + str(trigger_day) + ". day of the week.")
        sub_names = self.get_sub_names()
        global sub_data
        sub_data = self.get_data("Webhook_Channels")
        index = 0
        global reddit, sub
        subs = []
        range = random.randint(0, 27)

        while index < range:
            subs.append(reddit.subreddit(
                str(sub_names[index]).replace("'", "").replace(",", "").replace("(", "").replace(")",
                                                                                                 "").replace(
                    " ", "")))

            sub = random.choice(subs)

            index = index + 1

        global isWednesday
        try:
            if isWednesday:
                sub_names.append("ich_iel")
                sub_names.append("de")
            else:
                sub_names.remove("ich_iel")
                sub_names.remove("de")
        except Exception as e:
            errorlog.log_error(e, "")
        await MyClient.change_presence(self, activity=discord.Game(name=responds[64]))
        await asyncio.gather(self.check_date())

    # On_Message_Received
    async def on_message(self, message):
        try:
            global conn
            global commands_list
            global responds
            global descriptions
            global context

            descriptions = open("../rsc/command_description.txt", 'r', encoding="utf8").read().split(";")
            commands = commands_list

            if message.author == client.user:
                return
            if message.author.bot:
                return

            if message.content.lower() == commands[0]:
                await message.channel.send(embed=respond_messages.help())

            if message.content.lower().startswith("$help -mittwoch"):
                await message.channel.send(embed=respond_messages.help_mittwoch())

            if message.content.lower().startswith("$help -roulette"):
                await message.channel.send(embed=respond_messages.help_roulette())

            if message.content.lower().startswith("$help -koz"):
                await message.channel.send(embed=respond_messages.help_koz())

            if message.content.startswith("$roulette"):
                await games.roulette(message)


            elif message.content.lower().startswith("$private hilfe"):
                await message.author.send(str(responds[6]))

            elif message.content.lower().startswith("$bot -mittwoch -fire"):
                if security.isAdmin(message.author) or str(message.author == bot_author):
                    await message.channel.send(message.guild.roles[0], file=discord.File('../rsc/mittwoch.png'))

            elif message.content.lower().startswith("$setzkanal"):

                await message.channel.send(embed=respond_messages.set_channel(message=message, conn=conn,
                                                                              bot_author=open('../private/author.txt',
                                                                                              encoding="utf8").read()))

            elif message.content.lower().startswith("$z"):

                await message.channel.send(embed=respond_messages.z())

            elif message.content.lower().startswith("$koz"):
                await games.koz(message)

            elif message.content.lower().startswith("$about"):

                await message.channel.send(embed=respond_messages.about())

            elif message.content.lower().startswith("$kanal"):
                await message.channel.send(embed=respond_messages.kanal(message=message, conn=conn, client=client))

            elif message.content.lower().startswith("$send_meme_manual") and bot_author == str(
                    message.author):  # triggers the sending of the meme manually
                await self.send_meme()
            elif message.content.lower().startswith("$status") and bot_author == str(
                    message.author):  # Sends a message containing the status of the meme-sending of the server
                await message.channel.send(self.get_server_status(message.guild.id))


            elif message.content.lower().startswith("$show_commands"):
                await message.channel.send(embed=respond_messages.show_commands())

            elif message.content.lower().startswith("$delkanal"):
                await message.channel.send(embed=respond_messages.delkanal(message=message, conn=conn))
            elif message.content.lower().startswith("$setz_webhook"):
                await message.channel.send(embed=respond_messages.set_webhook(message=message, conn=conn))
            elif message.content.lower().startswith("$webhook"):
                await message.channel.send(embed=respond_messages.webhook(message=message, conn=conn, client=client))

            elif message.content.lower().startswith("$del_webhook"):
                await message.channel.send(embed=respond_messages.del_webhook(message=message, conn=conn))

            elif message.content.lower().startswith("$ping"):

                await message.channel.send(embed=respond_messages.ping(client=client))



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
            errorlog.log_error(e, message.content.lower())

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

    def get_data(self, table):
        global conn

        c = conn.cursor()

        c.execute('SELECT * FROM ' + table)

        return c.fetchall()

    async def send_meme(self):
        data = self.get_data("Info")

        notes = str("Last_Updated: " + str(datetime.datetime.today()))

        for i in data:
            try:
                channel_id = int(
                    security.decode(str(i).replace("'", "").split(",")[1].replace("(", "").replace(")", "")))

                channel = client.get_channel(channel_id)

                server_id = int(
                    str(security.decode(str(i).replace("'", "").split(",")[0].replace("(", "").replace(")", ""))))
                guild_role = client.get_guild(server_id).roles[0]

                status = self.get_server_status(server_id=server_id)
                if status == "0":
                    print("Sending on server: " + str(server_id) + " Time: " + str(datetime.datetime.today()))
                    await channel.send(guild_role, file=discord.File('../rsc/mittwoch.png'))
                    self.update_server_status(server_id, True, notes)
            except Exception as e:
                notes = str(e)
                errorlog.log_error(e, "")

    def update_server_status(self, server_id, status, notes):
        c = conn.cursor()
        const_server_id = server_id
        Server_id = security.encode(server_id)
        Server_id = (Server_id,)

        c.execute('DELETE FROM ' + 'Status' + ' WHERE Server_id=?', Server_id)

        conn.commit()

        print(str("Deleting Data for " + security.encode(server_id) + " Time: " + str(datetime.datetime.today())))

        self.set_server_status(const_server_id, status, notes)

    def get_server_status(self, server_id):
        global conn
        result = False
        c = conn.cursor()
        server_id = security.encode(server_id)
        server_id = (server_id,)

        c.execute('SELECT Sent FROM Status WHERE Server_id=?', server_id)
        try:
            result = (str(str((c.fetchone())).replace("[", "").replace("(", "").
                          replace("'", "").replace(",", "").replace(")", "").replace("]", "")))
        except Exception as e:
            errorlog.log_error(e, "")
        print(str("Result: " + str(result)))
        return result

    def set_server_status(self, server_id, status, notes):
        global conn

        c = conn.cursor()

        server_id = security.encode(server_id)

        values = [server_id, status, notes]

        c.execute('INSERT INTO Status VALUES (?,?,?)', values)

        conn.commit()

        print("Setting Status for: " + server_id + " Time: " + str(datetime.datetime.today()))

    def get_sub_names(self):
        global conn

        c = conn.cursor()

        c.execute('SELECT Sub_Name FROM sub_names')

        return c.fetchall()

    async def webhook(self):
        sub_range = random.randint(1, 1000)

        start_time = time.time() * 1000
        top = sub.top(limit=sub_range)
        print(top)

        allsubs = []
        for submission in top:
            allsubs.append(submission)
        randomsub = random.choice(allsubs)

        if not self.is_image(randomsub.url):
            randomsub = random.choice(allsubs)
            allowed = False
        else:
            allowed = True

        print("Loading Done! \nNeeded " + str(time.time() * 1000 - start_time) + " ms")
        if allowed:
            name = randomsub.title
            url = randomsub.url
            print(url)
            global sub_data
            for i in sub_data:
                try:
                    info = i
                    channel_id = int(
                        security.decode(str(info).replace("'", "").split(",")[1].replace("(", "").replace(")", "")))
                    channel = client.get_channel(channel_id)

                    em = discord.Embed(
                        title=name,
                        color=discord.Color.blurple()
                    )
                    #  em.add_field(name="Beschreibung:", value=str(sub.description))
                    em.set_footer(text="r/" + str(sub.display_name))
                    em.set_image(url=url)
                    await channel.send(embed=em)
                except Exception as e:
                    errorlog.log_error(e, "")

    def is_image(self, url):
        if ".jpg" in url or ".png" in url or ".jpeg" in url:
            return True
        else:
            return False

    def reset_server_status(self):
        server_ids = self.get_all_servers()

        for i in server_ids:
            self.update_server_status(i, "0", "Last_Updated: " + str(datetime.datetime.today()))
            print(str("Updating for: " + security.encode(i) + " Time: " + str(datetime.datetime.today())))

    def get_all_servers(self):
        global conn
        ids = []
        c = conn.cursor()
        c.execute('SELECT Server_id FROM Info')
        server_id = security.decode(
            str(c.fetchall()).replace("[", "").replace("]", "").replace("'", "").replace("(", "").replace(")",
                                                                                                          "").replace(
                ",", ""))
        ids.append(server_id)
        return ids

    async def check_date(self):  # checks if it is wednesday and controls the sending of the other memes
        global sent_available
        day = (datetime.datetime.today().weekday())
        minute = datetime.datetime.today().minute
        global trigger_day
        global isWednesday

        if str(day) == str(int(int(trigger_day) - 1)) and sent_available:
            isWednesday = True
            await self.send_meme()  # it's Wednesday ma dudes
            sent_available = False

        elif str(day) != str(int(int(trigger_day) - 1)):
            isWednesday = False  # reset values
            sent_available = True
            self.reset_server_status()
        global sending_meme
        if minute % 50 == 0 and minute > 0:  # sends two memes every hour
            start_time = time.time() * 1000
            if not sending_meme:
                index = 0
                sending_meme = True
                while index <= 2:
                    print(sending_meme)
                    index = index + 1
                    await self.webhook()
            print("Needed: " + str(time.time() * 1000 - start_time))
        else:
            sending_meme = False
        await asyncio.sleep(15)
        await asyncio.gather(self.check_date())


client = MyClient(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

descriptions = open('../rsc/command_description.txt', 'r', encoding="utf8").read().split(";")


@slash.slash(name="help", description=descriptions[0])
async def _help(ctx):
    await ctx.send(embed=respond_messages.help())


@slash.slash(name="help_mittwoch", description=descriptions[1])
async def _help_mittwoch(ctx):
    await ctx.send(embed=respond_messages.help_mittwoch())


@slash.slash(name="help_roulette", description=descriptions[2])
async def _help_roulette(ctx):
    await ctx.send(embed=respond_messages.help_roulette())


@slash.slash(name="help_koz", description=descriptions[3])
async def _help_koz(ctx):
    await ctx.send(embed=respond_messages.help_koz())


@slash.slash(name="roulette", description=descriptions[4])
async def _roulette(ctx):
    await ctx.send("Hier ist noch Baustelle :)", file=discord.File('../rsc/baustelle.jpg'))


@slash.slash(name="private_hilfe", description=descriptions[5])
async def _private_hilfe(ctx):
    await ctx.send("Hier ist noch Baustelle :)", file=discord.File('../rsc/baustelle.jpg'))


@slash.slash(name="bot_mittwoch_fire", description=descriptions[6])
async def _bot_mittwoch_fire(ctx):
    await ctx.send("Hier ist noch Baustelle :)", file=discord.File('../rsc/baustelle.jpg'))


@slash.slash(name="setzkanal", description=descriptions[7])
async def _setzkanal(ctx):
    await ctx.send("Hier ist noch Baustelle :)", file=discord.File('../rsc/baustelle.jpg'))


@slash.slash(name="delkanal", description=descriptions[8])
async def _delkanal(ctx):
    await ctx.send("Hier ist noch Baustelle :)", file=discord.File('../rsc/baustelle.jpg'))


@slash.slash(name="z", description=descriptions[9])
async def _z(ctx):
    await ctx.send(embed=respond_messages.z())


@slash.slash(name="koz", description=descriptions[10])
async def _koz(ctx):
    print(f"I got you, you said !")
    await ctx.send("Hier ist noch Baustelle :)", file=discord.File('../rsc/baustelle.jpg'))


@slash.slash(name="about", description=descriptions[11])
async def _about(ctx):
    await ctx.send(embed=respond_messages.about())


@slash.slash(name="kanal", description=descriptions[12])
async def _kanal(ctx):
    await ctx.send("Hier ist noch Baustelle :)", file=discord.File('../rsc/baustelle.jpg'))


@slash.slash(name="show_commands", description=descriptions[13])
async def _show_commands(ctx):
    await ctx.send(embed=respond_messages.show_commands())


@slash.slash(name="setz_webhook", description=descriptions[14])
async def _setz_webhook(ctx):
    await ctx.send("Hier ist noch Baustelle :)", file=discord.File('../rsc/baustelle.jpg'))


@slash.slash(name="del_webhook", description=descriptions[15])
async def _del_webhook(ctx):
    await ctx.send("Hier ist noch Baustelle :)", file=discord.File('../rsc/baustelle.jpg'))


@slash.slash(name="webhook", description=descriptions[16])
async def _webhook(ctx):
    await ctx.send("Hier ist noch Baustelle :)", file=discord.File('../rsc/baustelle.jpg'))


@slash.slash(name="ping", description=descriptions[17])
async def _ping(ctx):
    await ctx.send(embed=respond_messages.ping(client=client))


client.run(discord_token)
