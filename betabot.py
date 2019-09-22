import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

print('Betabot is starting up.')
key = 'BETABOT_TOKEN'

if key in os.environ:
    token = os.environ[key]
else:
    token = None

if token == None or token == '':
    print(f"Missing token environment variable '{key}'")
else:
    client.run(token)


