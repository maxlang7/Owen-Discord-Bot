# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord import Status


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
DELETE_DELAY = os.getenv('DELETE_DELAY')



client = discord.Client()
f = open(r'greetings.txt')
greetings = f.readlines()
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
    if member_before.status == Status.offline and member_after.status == Status.online:
        greeting = random.choice(greetings).rstrip()
        channel = discord.utils.get(client.get_all_channels(), guild__name="maxlang's server", name='general')
        message = await channel.send(f'{greeting}, {member_after.name} welcome back to {guild.name}')
        await message.delete(delay=DELETE_DELAY)


client.run(TOKEN)