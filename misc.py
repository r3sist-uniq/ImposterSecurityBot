import discord
import re
import requests
import imagehash
from io import BytesIO
from PIL import Image
import Levenshtein


def generate_regex_pattern(name):
    pattern = '^[-_ *]?' + ''.join(f'{c}[-_ *]?' for c in name.lower()) + '[-_ *]?$'
    return pattern


async def compare_profile_pic(member, owner):

    owner_avatar_url = owner.avatar.url
    member_avatar_url = member.avatar.url
    owner_avatar_response = requests.get(owner_avatar_url)
    member_avatar_response = requests.get(member_avatar_url)

    owner_avatar_image = Image.open(BytesIO(owner_avatar_response.content))
    member_avatar_image = Image.open(BytesIO(member_avatar_response.content))

    owner_avatar_hash = imagehash.phash(owner_avatar_image)
    member_avatar_hash = imagehash.phash(member_avatar_image)

    distance = Levenshtein.hamming(str(owner_avatar_hash), str(member_avatar_hash))
    similarity = 1.0 - (distance / len(str(owner_avatar_hash)))

    similarity_threshold = 0.9

    if similarity >= similarity_threshold:
        return 1
    else:
        return 0


async def alert_message(member,type, guild, is_profile_same):
    if is_profile_same == 0:
        profile_matches = "NO"
    else:
        profile_matches = "YES"

    if type=='alert':
        channel_name = "impersonation-alerts"   
        message = f"Impersonator kicked:\nUsername: {member}\nTag: {member.discriminator}\n Nickname: {member.display_name}\nID= {member.id}\n Photo matches? {profile_matches}"
    elif type =='assist':
        channel_name = "impersonation-assist"
        message = f"(LOW ALERT) I think this person might be impersonating. Please check if you need to kick this person? :\nUsername: {member}\nTag: {member.discriminator}\nNickname: {member.display_name}\n ID = {member.id}\n Photo matches? {profile_matches}"
    elif type =='high-assist':
        channel_name = "impersonation-assist"
        message = f"(HIGH ALERT) I think this person might be impersonating. Please check if you need to kick this person? :\nUsername: {member}\nTag: {member.discriminator}\nNickname: {member.display_name}\n ID = {member.id}\n Photo matches? {profile_matches}"
    channel = discord.utils.get(guild.channels, name=channel_name)

    print(message)
    if not channel:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            guild.owner: discord.PermissionOverwrite(read_messages=True),
            guild.roles[0]: discord.PermissionOverwrite(read_messages=False)
        }          
        new_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)

        await new_channel.send(message)
    else:
        await channel.send(message)


def owner_regex_patterns(owner):
    owner_name = owner.name.lower()
    owner_nick = owner.display_name.lower()
    
    owner_name_format = generate_regex_pattern(owner_name)
    owner_nick_format = generate_regex_pattern(owner_nick)

    owner_name_regex = re.compile(owner_name_format, re.IGNORECASE)
    owner_nick_regex = re.compile(owner_nick_format, re.IGNORECASE)

    return owner_name_regex, owner_nick_regex, owner_name, owner_nick
