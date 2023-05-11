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
            print(owner.avatar.url, guild)
            owner_name = owner.name.lower()
            owner_nick = owner.display_name.lower()
            
            owner_name_format = util.generate_regex_pattern(owner_name)
            owner_nick_format = util.generate_regex_pattern(owner_nick)

            owner_name_regex = re.compile(owner_name_format, re.IGNORECASE)
            owner_nick_regex = re.compile(owner_nick_format, re.IGNORECASE)
            
            for member in guild.members:
                member_name = member.name.lower()
                member_nick = member.display_name.lower()

                if member != owner and not (member.guild_permissions.administrator or member.guild_permissions.manage_messages) and (str(member) == str(owner) or
                                        owner_name_regex.search(member_name) or
                                        owner_nick_regex.search(member_name) or
                                        owner_name_regex.search(member_nick) or
                                        owner_nick_regex.search(member_nick)):

                    message = f"Impersonator kicked:\nUsername: {member}\nTag: {member.discriminator}\n Nickname: {member.display_name}, {guild}, {owner_name}, {owner_nick}, {member_nick} "
                    await member.kick(reason='Impersonating the server owner')
                    channel_name = "impersonation-alerts"   
                    channel = discord.utils.get(guild.channels, name=channel_name)

                    if not channel:
                        overwrites = {
                            guild.default_role: discord.PermissionOverwrite(read_messages=False),
                            guild.me: discord.PermissionOverwrite(read_messages=True),
                            guild.owner: discord.PermissionOverwrite(read_messages=True),
                            guild.roles[0]: discord.PermissionOverwrite(read_messages=False)  # Set the @everyone role to not see the channel
                        }          
                        new_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
                        await new_channel.send(message)
                    else:
                        await channel.send(message)

                elif member != owner and not (member.guild_permissions.administrator or member.guild_permissions.manage_messages) and ((Levenshtein.distance(member_name, owner_name) <= 2) or (Levenshtein.distance(member_name, owner_nick) <= 2) or (Levenshtein.distance(member_nick, owner_name) <= 2) or (Levenshtein.distance(member_nick, owner_nick) <= 2)):


                    profile_same = await util.compare_profile_pic(member, owner)
                    if profile_same == 1:
                        message = f"Impersonator kicked:\nUsername: {member}\nTag: {member.discriminator}\n Nickname: {member.display_name}, {guild}, {owner_name}, {owner_nick}, {member_nick} "
                        await member.kick(reason='Impersonating the server owner')
                        channel_name = "impersonation-alerts"   
                        channel = discord.utils.get(guild.channels, name=channel_name)

                        message = f"Impersonator kicked:\nUsername: {member}\nTag: {member.discriminator}\n Nickname: {member.display_name}, {guild}, {owner_name}, {owner_nick}, {member_nick} "
                        await member.kick(reason='Impersonating the server owner')
                        channel_name = "impersonation-alerts"   
                        channel = discord.utils.get(guild.channels, name=channel_name)

                        if not channel:
                            overwrites = {
                                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                guild.me: discord.PermissionOverwrite(read_messages=True),
                                guild.owner: discord.PermissionOverwrite(read_messages=True),
                                guild.roles[0]: discord.PermissionOverwrite(read_messages=False)  # Set the @everyone role to not see the channel
                            }          
                            new_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
                            await new_channel.send(message)
                        else:
                            await channel.send(message)
                    else:
                        message = f"I think this person is impersonating. Do you want to kick this person? :\nUsername: {member}\nTag: {member.discriminator}\n Nickname: {member.display_name}, {guild}, {owner_name}, {owner_nick}, {member_nick} "
                        channel_name = "impersonation-assist"   
                        channel = discord.utils.get(guild.channels, name=channel_name)

                        if not channel:
                            overwrites = {
                                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                guild.me: discord.PermissionOverwrite(read_messages=True),
                                guild.owner: discord.PermissionOverwrite(read_messages=True),
                                guild.roles[0]: discord.PermissionOverwrite(read_messages=False)  # Set the @everyone role to not see the channel
                            }          
                            new_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
                            await new_channel.send(message)
                        else:
                            await channel.send(message)
                

        except Exception as e:
            print('some error happened: ', e)

              
bot.run(bot_token)

