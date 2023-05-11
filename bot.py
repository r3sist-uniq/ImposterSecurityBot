import discord
from discord.ext import commands, tasks
import re, os
from dotenv import load_dotenv
import Levenshtein
import requests
import imagehash
from io import BytesIO
from PIL import Image
import util

load_dotenv()
bot_token = os.environ['bot_token']

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():

    print(f'Bot connected as {bot.user}')
    check_impersonators.start()

@tasks.loop(seconds=10)
async def check_impersonators():
    for guild in bot.guilds:
        try:
            owner = guild.owner
            owner_name_regex, owner_nick_regex = util.owner_regex_patterns(owner=owner)

            for member in guild.members:
                member_name = member.name.lower()
                member_nick = member.display_name.lower()

                if member != owner and not (member.guild_permissions.administrator or member.guild_permissions.manage_messages) and (str(member) == str(owner) or
                                        owner_name_regex.search(member_name) or
                                        owner_nick_regex.search(member_name) or
                                        owner_name_regex.search(member_nick) or
                                        owner_nick_regex.search(member_nick)):

                    await member.kick(reason='Impersonating the server owner')
                    await util.alert_message(member, 'alert', guild)

                elif member != owner and not (member.guild_permissions.administrator or member.guild_permissions.manage_messages) and ((Levenshtein.distance(member_name, owner_name) <= 2) or (Levenshtein.distance(member_name, owner_nick) <= 2) or (Levenshtein.distance(member_nick, owner_name) <= 2) or (Levenshtein.distance(member_nick, owner_nick) <= 2)):

                    profile_same = await util.compare_profile_pic(member, owner)
                    if profile_same == 1:
                        await member.kick(reason='Impersonating the server owner')

                        await util.alert_message(member, 'alert', guild)
                    else:
                        await util.alert_message(member, 'assist', guild)

        except Exception as e:
            print('some error happened: ', e)

              
bot.run(bot_token)

