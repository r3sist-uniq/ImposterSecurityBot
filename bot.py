import discord
from discord.ext import commands, tasks
import re, os
from dotenv import load_dotenv

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
            owner_name = owner.display_name.lower()
            owner_nick = owner.name.lower()
            
            owner_name_format = generate_regex_pattern(owner_name)
            owner_nick_format = generate_regex_pattern(owner_nick)

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

                    message = f"Impersonator kicked:\nUsername: {member}\nTag: {member.discriminator}\n Nickname: {member.display_name}"

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
        except Exception as e:
            print('some error happened: ', e)

              
bot.run(bot_token)

def generate_regex_pattern(name):
    pattern = '^[-_ ]?' + ''.join(f'{c}[-_ ]?' for c in name.lower()) + '[-_ ]?$'
    return pattern

