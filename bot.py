# bot.py
import os
import random
import discord
import time
import datetime
from dotenv import load_dotenv
from discord import Status
import pytz


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
DELETE_DELAY = int(os.getenv('DELETE_DELAY'))

client = discord.Client()

client.last_splash_post = datetime.date.today() - datetime.timedelta(days=1)

eastern = pytz.timezone('US/Eastern')

f = open(r'greetings.txt')
greetings = f.readlines()
f.close()

f = open(r'splashes.txt')
splashes = f.readlines()
f.close() 

f = open(r'holidays.csv')
holidays = f.readlines()
f.close()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} has connected to the following guild:\n'
        f'{guild.name}(id: {guild.id}'
        )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Greetings {member.name}, greatness awaits you in this land of promise.'
    )


@client.event
async def on_member_update(member_before, member_after):
    guild = discord.utils.get(client.guilds, name=GUILD)
    channel = discord.utils.get(client.get_all_channels(), guild__name="maxlang's server", name='general')
    splash_channel = discord.utils.get(client.get_all_channels(), guild__name="maxlang's server", name='minecraftsplashes')
    await daily_splash(client, splash_channel)
    await greet_user(client, channel, member_before, member_after, guild)


async def daily_splash(client, channel):
    if client.last_splash_post < datetime.date.today() and datetime.datetime.now(tz=eastern).hour > 5:
            splash = random.choice(splashes).rstrip()
            message = await channel.send(splash)
            await message.delete(delay=24*60*60)
            client.last_splash_post = datetime.date.today()


async def greet_user(client, channel, member_before, member_after, guild):
   if member_before.status == Status.offline and member_after.status == Status.online:
        greeting = random.choice(greetings).rstrip()
        message = await channel.send(f'{greeting}, {member_after.name} welcome back to {guild.name}')
        await message.delete(delay=DELETE_DELAY)
        print(client.last_splash_post)

client.run(TOKEN)