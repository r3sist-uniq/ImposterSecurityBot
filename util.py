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