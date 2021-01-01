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

  if msg.startswith('vorig spel'):
    get_user_name = msg.split('vorig spel ',1)[1]
    rank = LastMatch(get_user_name).conquest_rank()
    await message.channel.send(rank)

# keep_alive()
client.run(TOKEN)

# if msg.startswith('vorig spel'):
#   rank = LastMatch('Cleendert').conquest_rank()
#   await message.channel.send(rank)