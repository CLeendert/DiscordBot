import discord
from env_vars import TOKEN
from GetRank import LastMatch
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('rank'):
        get_user_name = msg.split('rank ', 1)[1]
        rank = LastMatch(get_user_name).conquest_rank()
        await message.channel.send(get_user_name + ' is ' + rank)

    if msg.startswith('is ben een noob?'):
        await message.channel.send('Jazeker')

    if msg.startswith('is leendert een noob?'):
        rankleendert = LastMatch(get_user_name).conquest_rank()
        await message.channel.send('Nee die is toch ' + rankleendert)

    if msg.startswith('last match'):

        get_user_name = msg.split('last match ', 1)[1]
        rankslastmatch = LastMatch(get_user_name).last_match_ranks()

        await message.channel.send(rankslastmatch)

client.run(TOKEN)

