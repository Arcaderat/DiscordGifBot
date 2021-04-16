import re

import discord


client = discord.Client()
commands = {}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print("message received")
    #print(message.content)
    #print(message.attachments)
    #set shortcut to attachment
    if message.content.startswith('$set'):
        #get the shortcut from between the semicolons
        pattern = ";(.*?);"
        shortcut = ";" + re.search(pattern, message.content).group(1) + ";"
        #save the shortcut in our dictionary with the attachment url
        commands[shortcut] = message.attachments[0].url
        await message.channel.send('Shortcut saved, type ' + shortcut + ' to send:')
        await message.channel.send(commands[shortcut])

    if message.content.startswith(';') and message.content.endswith(';'):
        if message.content in commands.keys():
            await message.channel.send(message.author.display_name)
            await message.channel.send(commands[message.content])
            await message.delete()
        print(message.content)

client.run("ODMyMzU3NzkzOTg0OTM4MDM0.YHinmg.19XKG_UtbRUDt4GfLB2aQUkicNs")
