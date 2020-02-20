import os

import discord
from dotenv import load_dotenv
from random import choice
import ast

VERSION = "1.1"

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
admins = ast.literal_eval(os.getenv('ADMINISTRATORS'))

with open('rep', 'r') as repFile:
    reps = ast.literal_eval(repFile.read())

client = discord.Client()

def mod_rep(id, change):
    if id in reps:
        reps[id] += change
    else:
        reps[id] = change
    
    with open('rep', 'w') as repFile:
        repFile.write(str(reps))

@client.event
async def on_ready():
    print(f'{client.user} (v{VERSION}) has connected to Discord')

@client.event
async def on_disconnect():
    print('disconnecting')


responses = ['did you mean pepsi', 'pepsi', 'i think you meant pepsi', 'no', 
             'fuck off', 'pepsi is superior', 'coke tastes like motor oil', 
             'who even drinks coke', 'do not speak of that hideous beverage', 
             'coke is the soda of sin', 'smart people drink pepsi',
             'shame', 'shun the non-believer', 'coke is worthless']
@client.event
async def on_message(message):
    if message.author == client.user:
        print(f'response: {message.content}')
        return
        
    cont = message.content.lower()
    print(f'{message.guild.name}:{message.channel.name}:{message.author.name}: {cont}')
    
    if 'pepsi' in cont and not 'bad' in cont and not 'stupid' in cont and not 'coke' in cont and not 'fuck' in cont:
        mod_rep(message.author.id, choice(range(0, 2)))
        
    if 'coke' in cont:
        await message.channel.send(choice(responses))
        if not message.author.id in reps or reps[message.author.id] == 0:
            await message.channel.send('your reputation decreases when you talk about the forbidden beverage.')
        mod_rep(message.author.id, choice(range(-5, -1)))
    
    if 'https://discord.gg' in cont:
        await message.channel.send(f'<@!{message.author.id}> it looks like you sent an invite to a discord server. this is prohibited')
        await message.channel.send('attempting message deletion...')
        try:
            await message.delete()
        except discord.Forbidden:
            await message.channel.send('deletion failed: improper permissions')
    
    if 'my' in cont and 'rep' in cont:
        id = message.author.id
        if id in reps:
            await message.channel.send(f"<@!{id}>'s reputation is {reps[id]}")
        else:
            await message.channel.send(f"<@!{id}> has no reputation yet")
    
    if cont[0] == '!' and message.author.id in admins:
        cmd = cont[1:].replace(' ', '')
        if cmd == 'dc':
            await message.channel.send('disconnecting...')
            await client.close()
        elif cmd == 'listadmins':
            for admin in admins:
                await message.channel.send(f'admin: {client.get_user(admin)}')
        elif 'showrolesfor' in cmd:
            id = int(cmd[15:-1])
            usr = message.channel.guild.get_member(id)
            msg = f'{usr.name} has the following role'
            if len(usr.roles[1:]) > 1: msg += 's: '
            elif len(usr.roles[1:]) == 1: msg += ': '
            else: msg = f'{usr.name} has no roles'
            i = 0
            for role in usr.roles[1:]:
                if i > 0: msg += ', '
                msg += role.name
                i += 1
            await message.channel.send(msg)
        elif 'cfile' in cmd:
            name = cmd[5:]
            file = open(name, 'w')
            file.close()
        elif 'append' in cmd:
            name = cmd.split('append')[0]
            cont = cmd.split('append')[1]
            cont = cont.replace('\\n', '\n')
            file = open(name, 'a')
            file.write(cont)
            file.close()
        elif 'modrep' in cmd:
            id = int(cmd.split(',')[0][9:-1])
            val = int(cmd.split(',')[1])
            mod_rep(id, val)
            await message.channel.send(f"<@!{id}>'s reputation is now {reps[id]}")
        elif 'getrep' in cmd:
            id = int(cmd[9:-1])
            if id in reps:
                await message.channel.send(f"<@!{id}>'s reputation is {reps[id]}")
            else:
                await message.channel.send(f"<@!{id}> has no reputation yet")
                
    elif cont[0] == '!':
        await message.channel.send(f'{message.author.name} is not an admin and cannot use !commands')

client.run(token)
