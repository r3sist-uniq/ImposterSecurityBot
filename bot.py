import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import misc
import Levenshtein

load_dotenv()
bot_token = os.environ['bot_token']

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

already_alerted = []
@bot.event
async def on_ready():

    print(f'Bot connected as {bot.user}')
    check_impersonators.start()

@bot.event
async def on_member_remove(member):
    guild = member.guild
    try:
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.kick):
            member_cache = {'guild': guild, 'member': member}
            if (entry.target == member) and (member_cache in already_alerted):
                print(f'{member.name} has been kicked.')
                print('removing')
                already_alerted.remove(member_cache)
                break
    except Exception as e:   
        print('some error happened: a', e)
        
@tasks.loop(seconds=10)
async def check_impersonators():
    for guild in bot.guilds:
        try:
            owner = guild.owner
            owner_name_regex, owner_nick_regex, owner_name, owner_nick= misc.owner_regex_patterns(owner=owner)

            for member in guild.members: 

                member_name = member.name.lower()
                member_nick = member.display_name.lower()

                if (member != owner and not (member.guild_permissions.administrator or member.guild_permissions.manage_messages)) and (str(member) == str(owner) or
                                        owner_name_regex.search(member_name) or
                                        owner_nick_regex.search(member_name) or
                                        owner_name_regex.search(member_nick) or
                                        owner_nick_regex.search(member_nick)):

                    is_profile_same = await misc.compare_profile_pic(member, owner)
                    await member.kick(reason='Impersonating the server owner')
                    await misc.alert_message(member, 'alert', guild, is_profile_same)

                elif member != owner and not (member.guild_permissions.administrator or member.guild_permissions.manage_messages) and ((Levenshtein.distance(member_name, owner_name) <= 2) or (Levenshtein.distance(member_name, owner_nick) <= 2) or (Levenshtein.distance(member_nick, owner_name) <= 2) or (Levenshtein.distance(member_nick, owner_nick) <= 2)):

                    is_profile_same = await misc.compare_profile_pic(member, owner)
                    
                    if is_profile_same == 1:
                        await member.kick(reason='Impersonating the server owner')
                        await misc.alert_message(member, 'alert', guild, is_profile_same)
                        
                    else:
                        alerted_person = {'guild': guild, 'member': member}
                        if not alerted_person in already_alerted:
                            await misc.alert_message(member, 'high-assist', guild, is_profile_same)
                            already_alerted.append(alerted_person)

                elif member != owner and not (member.guild_permissions.administrator or member.guild_permissions.manage_messages) and ((Levenshtein.distance(member_name, owner_name) <= 3) or (Levenshtein.distance(member_name, owner_nick) <= 3) or (Levenshtein.distance(member_nick, owner_name) <= 3) or (Levenshtein.distance(member_nick, owner_nick) <= 3)): 
                    is_profile_same = await misc.compare_profile_pic(member, owner)
                    alerted_person = {'guild': guild, 'member': member}
                    if not (alerted_person in already_alerted) and is_profile_same == 1:
                        # await member.kick(reason='Impersonating the server owner')
                        # await misc.alert_message(member, 'alert', guild, is_profile_same)
                        await misc.alert_message(member, 'high-assist', guild, is_profile_same)
                        already_alerted.append(alerted_person)
                    elif not (alerted_person in already_alerted) and is_profile_same == 0:
                        await misc.alert_message(member, 'assist', guild, is_profile_same)
                        already_alerted.append(alerted_person)

        except Exception as e:
            print('some error happened: ', e)

bot.run(bot_token) 

