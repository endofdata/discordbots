import discord
from discord.ext import commands
import os
import json
import random
import base64
import asyncio

# Checking if in right dir
os.chdir("/home/pi/Documents/Python Projects/sundaybot")

#------------------------------------------------------------------------------
# Environment variables used by SundayBot
#------------------------------------------------------------------------------
env_token = 'SUNDAYBOT_TOKEN'

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
# Create a discord client
#------------------------------------------------------------------------------
# Create the client and let it use the event loop with the timeout.
# client = discord.Client()

# Create the client using the Bot subclass
client = commands.Bot(command_prefix='$')

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
# @client.event
async def on_message(message):

    # If message author is our client user, it's our own message. Ignore it.
    if message.author == client.user:
        return

    # If the message text starts wiht '$hello', reply with 'Hello!'.
    if message.content.startswith('$hello'):
        await message.channel.send(f'Hello, {message.author.name}!')
    elif message.content.startswith('$pn'):
        await message.author.send(f'Hello, {message.author.name}! You want to talk to me?')

@client.command()
async def profile(ctx):
    await create_account(ctx.author)
    user = ctx.author
    users = await get_userdata()
    
    town_name = users[str(user.id)]["townname"]
    file = discord.File(users[str(user.id)]["picture"], filename="Figur1.png")
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]
    
    embed = discord.Embed(title = f"{ctx.author.name}'s profile", colour = discord.Colour.blue())
    embed.add_field(name = "townname", value = town_name, inline = False)
    embed.set_image(url="attachment://Figur1.png")
    embed.add_field(name = "wallet", value = wallet_amt, inline = False)
    embed.add_field(name = "bank", value = bank_amt, inline = True)
    await ctx.send(file=file, embed = embed)
    
@client.command()
async def beg (ctx):
    create_account(ctx.author)
    user = ctx.author
    users = await get_userdata()
    
    earnings = random.randint(0, 99)
    
    await ctx.send(f"Someone gave you {earnings} coins!")
    
    users[str(user.id)]["wallet"] += earnings
    
@client.command()
async def start (ctx):
    create_account(ctx.author)
    user = ctx.author
    users = await get_userdata()
    
    earnings = random.randint(0, 99)
    
    await ctx.send(f"Someone gave you {earnings} coins!")
    
    users[str(user.id)]["wallet"] += earnings
    await store_userdata(users)

#------------------------------------------------------------------------------
# Helper-Funktions
#------------------------------------------------------------------------------

async def create_account(user):
    users = await get_userdata()
    
    if str(user.id) in users:
        return False
    else:
        
        townname = "default"
        
        em = discord.Embed(title = "Charakterwahl", colour = discord.Colour.blue())
        em.set_text(name = "Es stehen 6 Charaktere zur auswahl, reagiere bitte mit der Zahl des Charakters, den du haben möchtest:")
        #folgendes Bild muss ich noch erstellen hier ist aber noch kein GIMP drauf....
        #em.set_image(url="attachment://allFigures.png")
        em.set_image(url="attachment://Figure1.png")
        await ctx.send(embed = em)
        
        #Ich weiß noch nicht, wie ich das auf eine Message beziehe
        if str(reaction.emoji) == "1️⃣":
            users[str(user.id)]["picture"] = "/home/pi/Documents/Python Projects/sundaybot/Pictures/Figur1.png"
        elif str(reaction.emoji) == "2️⃣":
            users[str(user.id)]["picture"] = "/home/pi/Documents/Python Projects/sundaybot/Pictures/Figur2.png"
        elif str(reaction.emoji) == "3️⃣":
            users[str(user.id)]["picture"] = "/home/pi/Documents/Python Projects/sundaybot/Pictures/Figur3.png"
        elif str(reaction.emoji) == "4️⃣":
            users[str(user.id)]["picture"] = "/home/pi/Documents/Python Projects/sundaybot/Pictures/Figur4.png"
        elif str(reaction.emoji) == "5️⃣":
            users[str(user.id)]["picture"] = "/home/pi/Documents/Python Projects/sundaybot/Pictures/Figur5.png"
        elif str(reaction.emoji) == "6️⃣":
            users[str(user.id)]["picture"] = "/home/pi/Documents/Python Projects/sundaybot/Pictures/Figur6.png"
        
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["townname"] = townname
        #users[str(user.id)]["picture"] = "/home/pi/Documents/Python Projects/sundaybot/Pictures/Figur1.png"
        
        await store_userdata(users)
        return True

async def get_userdata():
    with open("Userdata.json", "r") as f:
        users = json.load(f)
    return users

async def store_userdata(users):
    with open("Userdata.json", "w") as f:
        json.dump(users, f)

def run_debug():
    testUser = {}
    testUser['id'] = "Holger"
    create_account(testUser)

#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
print('Sundaybot is starting up.')

# Read environment variable for authentication token
token = get_env(env_token)

# We cannot run without a valid authentication token.
if token == None or token == '':
    print(f"Missing token environment variable '{env_token}'. Running debug mode.")
    #asyncio.run(run_debug())
    run_debug()
        
else:
    
    # Run the discord client to receive discord events.
    client.run(token)

    # Client.run() is blocking until the end of the event loop
    print('Sundaybot is going to sleep.')

   #await client.close()
    
