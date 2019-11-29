import discord
import os
import threading
import logging
import asyncio

#------------------------------------------------------------------------------
# Create a discord client
#------------------------------------------------------------------------------
client = discord.Client()

#------------------------------------------------------------------------------
# Discord event handlers
#------------------------------------------------------------------------------

# Discord data received and prepared (usually occurs after login)
# See https://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# A message is created and sent
# See https://discordpy.readthedocs.io/en/latest/api.html#discord.on_message
@client.event
async def on_message(message):

    # If message author is our client user, it's our own message. Ignore it.
    if message.author == client.user:
        return

    # If the message text starts wiht '$hello', reply with 'Hello!'.
    if message.content.startswith('$hello'):
        await message.channel.send(f'Hello, {message.author.name}!')

#------------------------------------------------------------------------------
# Utility methods
#------------------------------------------------------------------------------

# Shut down the client connection 
# This is not raised by discord, but from a timer in this bot
def on_shutdown():
    print('Betabot is closing client connection.')
    asyncio.run(client.close())

# Example, how to init logging to a file
# https://discordpy.readthedocs.io/en/latest/logging.html#logging-setup
def init_logging():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

# Get the value of an environment variable
# Parameters
#   key: name of the variable 
# Returns
#   The value, or None if the variable is not set.
def get_env(key):
    if key in os.environ:
        val = os.environ[key]
    else:
        val = None

    return val

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
print('Betabot is starting up.')

env_token = 'BETABOT_TOKEN'
env_timeout = 'BETABOT_TIMEOUT'

# Read environment variables for authentication token and shutdown timeout
token = get_env(env_token)
timeout = get_env(env_timeout)

# If BETABOT_TIMEOUT is not set, use a default of 8 hours.
if timeout == None or timeout == '':
    print(f"No timeout environment variable '{env_timeout}'. Using default timeout (8 h).")
    timeout_seconds = 8 * 60 * 60
else:
    timeout_seconds = float(timeout) * 60

# We cannot run without a valid authentication token.
if token == None or token == '':
    print(f"Missing token environment variable '{env_token}'.")
else:
    # Start a timer to automatically shut down the bot.
    shutdown_timer = threading.Timer(timeout_seconds, on_shutdown)
    shutdown_timer.start()

    # Run the discord client to receive discord events.
    client.run(token)

    print('Betabot is going to sleep.')

    # Clear the time in case of client.run() returned w/o timeout.
    shutdown_timer.cancel()
