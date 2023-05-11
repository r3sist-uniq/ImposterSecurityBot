def generate_regex_pattern(name):
    pattern = '^[-_ *]?' + ''.join(f'{c}[-_ *]?' for c in name.lower()) + '[-_ *]?$'
    return pattern


async def compare_profile_pic(member, owner):

    # Download profile pictures
    owner_avatar_url = owner.avatar.url
    member_avatar_url = member.avatar.url
    owner_avatar_response = requests.get(owner_avatar_url)
    member_avatar_response = requests.get(member_avatar_url)

    # Compare profile pictures using Levenshtein distance
    owner_avatar_image = Image.open(BytesIO(owner_avatar_response.content))
    member_avatar_image = Image.open(BytesIO(member_avatar_response.content))

    owner_avatar_hash = imagehash.phash(owner_avatar_image)
    member_avatar_hash = imagehash.phash(member_avatar_image)

    distance = Levenshtein.hamming(str(owner_avatar_hash), str(member_avatar_hash))
    similarity = 1.0 - (distance / len(str(owner_avatar_hash)))

    # Compare similarity threshold
    similarity_threshold = 0.9

    if similarity >= similarity_threshold:
        print("The member's profile picture matches the owner's profile picture!")
        return 1
    else:
        print("The member's profile picture does not match the owner's profile picture.")
        return 0

async def alert_message(member,type, guild, ):
    
    if type=='alert':
        channel_name = "impersonation-alerts"   
        message = f"Impersonator kicked:\nUsername: {member}\nTag: {member.discriminator}\n Nickname: {member.display_name}"
    elif type =='assist':
        channel_name = "impersonation-assist"
        message = f"I think this person is impersonating. Do you want to kick this person? :\nUsername: {member}\nTag: {member.discriminator}\n Nickname: {member.display_name}"

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