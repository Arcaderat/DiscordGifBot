import re
import json
import discord


client = discord.Client()

with open("./commands.json") as f:
    commands = json.load(f)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    #ignore own messages
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
        #dump commands into commands.json to maintain state if server goes down
        with open("./commands.json", "w") as commands_file:
            json.dump(commands, commands_file);
        await message.channel.send('Shortcut saved, type ' + shortcut + ' to send:')
        await message.channel.send(commands[shortcut])

    if message.content.startswith(';') and message.content.endswith(';'):
        if message.content in commands.keys():
            await message.channel.send(message.author.display_name)
            await message.channel.send(commands[message.content])
            await message.delete()
        print(message.content)

client.run("ODMyMzU3NzkzOTg0OTM4MDM0.YHinmg.19XKG_UtbRUDt4GfLB2aQUkicNs")
