# ImposterSecurityBot
<p align="center">
  <img src="https://github.com/r3sist-uniq/ImposterSecurityBot/assets/72573738/bb53d5dc-6075-4013-829f-d6ec5350572d" alt="imposter-security-logo"/>
</p>

# Discord Bot for Kicking Owner Impersonators

This Discord bot is designed to automatically kick members who are impersonating the server owner in Discord servers. It identifies potential impersonators by comparing their usernames and nicknames with the server owner's information using regular expressions. Made by Sehaj (dxstiny) and Aman (r3sist).

## Setup

You can use this URL to invite the bot in your server [Invite](https://discord.com/api/oauth2/authorize?client_id=1104343553875914793&permissions=402655382&scope=bot)


1. Invite the Bot: Use the provided URL to invite the bot to your Discord server. Make sure to give access to every permission the bot requires. 
2. Set Up Bot Permissions: After inviting the bot, ensure that the bot has a role with sufficient permissions to kick members. 
3. The bot's role should have higher hierarchy than the roles of potential impersonators, meaning most members. Go to server settings --> roles --> drag the role of the bot "impostersecurity" to the top below admin role. (drag ahove by clicking the left button as shown below)


![imageeeee](https://github.com/r3sist-uniq/ImposterSecurityBot/assets/72573738/462e2332-7875-4d68-9e03-4434b6d74c1f)

## How it works

Impersonator Detection: The bot periodically (every 10 seconds) checks all the guilds (servers) it is a member of for potential owner impersonators. It compares the usernames and nicknames of each member with the server owner's information using regular expressions.

Impersonator Kicking: If a member is identified as an impersonator (not the server owner and matches the impersonation patterns), the bot will kick the impersonator from the server and send a message to a channel named "impersonation-alerts". If the channel doesn't exist, the bot will create it with the necessary permissions.

We are using the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) and the [Hamming Distance](https://en.wikipedia.org/wiki/Hamming_distance) algorithms to check for the similarities between strings, and profile pictures, respectively. 

## Support and Issues

If you encounter any issues or need support, feel free to contact the developer of the bot or open an issue in the bot's repository.

## Contribute 

If you want to improve the bot's functioning, please create a pull request. 

## Disclaimer

This bot is provided as-is without any warranty. The developer of the bot is not responsible for any misuse or damage caused by the bot. Use it responsibly and in accordance with Discord's terms of service.
