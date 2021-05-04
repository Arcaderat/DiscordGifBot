import re
import json
import discord
import requests


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
    #print("message received")
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

    #commands start and end with ;
    if message.content.startswith(';') and message.content.endswith(';'):
        if message.content in commands.keys():
            await message.channel.send(message.author.display_name)
            await message.channel.send(commands[message.content])
            await message.delete()
        print(message.content)

    #check if message is a tiktok link
    if message.content.startswith('https://vm.tiktok.com/'):
        sent_url = message.content
        #the shortened mobile url doesn't work for the api, so get the full url
        real_url = requests.get(sent_url).url
        #request to tiktok api
        response = requests.get('https://www.tiktok.com/oembed?url=' + real_url)
        if response.status_code == 200:
            video_info = response.json()
            video_description = video_info["title"]
            video_title = video_info["author_name"] + " on Tiktok"
            video_thumbnail = video_info["thumbnail_url"]
            video_embed = discord.Embed(title=video_title, description=video_description, url=sent_url,
                                        name="TikTok", color=0x1a1a1a)
            video_embed.set_thumbnail(url=video_thumbnail)
            await message.channel.send(embed=video_embed)


client.run("ODMyMzU3NzkzOTg0OTM4MDM0.YHinmg.19XKG_UtbRUDt4GfLB2aQUkicNs")
