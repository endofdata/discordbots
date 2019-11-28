import discord
import os
import threading

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


def on_shutdown():
    print('Betabot is closing client connection.')
    client.close()

def get_env(key):
    if key in os.environ:
        val = os.environ[key]
    else:
        val = None

    return val

print('Betabot is starting up.')
env_token = 'BETABOT_TOKEN'
env_timeout = 'BETABOT_TIMEOUT'

token = get_env(env_token)
timeout = get_env(env_timeout)

if timeout == None or timeout == '':
    print(f"No timeout environment variable '{env_timeout}'. Using default timeout")
    timeout_seconds = 8 * 60 * 60
else:
    timeout_seconds = float(timeout) * 60

if token == None or token == '':
    print(f"Missing token environment variable '{key}'")
else:
    shutdown_timer = threading.Timer(timeout_seconds, on_shutdown)
    shutdown_timer.start()
    client.run(token)
    shutdown_timer.cancel()

print('Betabot is going to sleep.')

