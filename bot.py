import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True

# client = discord.Client(intents=intents)
client = commands.Bot('!', intents=intents)

@client.event
async def on_read():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    fields = message.content.split()
    nBytes = 16
    response_text = None

    # get some bytes from random.org
    if message.content.startswith('!grn'):
        if len(fields) > 1:
            nBytes = fields[1]
        r = requests.get(f"https://www.random.org/cgi-bin/randbyte?nbytes={nBytes}&format=h%22")
        response_text = r.text
        await message.channel.send(f"```\n{response_text}```")

    # send the results of a GET request
    # (defaults to byte-sending)
    elif message.content.startswith('!get'):
        get_request = f"https://www.random.org/cgi-bin/randbyte?nbytes={nBytes}&format=h%22"
        if len(fields) > 1:
            get_request = fields[1]
        
        r = requests.get(get_request)
        response_text = r.text
        await message.channel.send(f"```\n{response_text}```")

    # # meme response
    # elif message.content.startswith('!a'):
    #     response_text = "https://cdn.discordapp.com/attachments/796352920202510357/1065568414762029127/IMG_8927.png"
    #     await message.channel.send(f"{response_text}")

    print(message)
    print(message.content)
    print()

    await client.process_commands(message)
 
# define file names and internal names of reaction dictionaries
dict_names_list =   ['images', 'images-2', 'special', 'info', 'words' ]
dict_list = [name + '.json' for name in dict_names_list]

async def main():
    import cogs.dictspeak as ds
    import cogs.bookkeeper as bk
    # client.add_cog(ds.DictSpeak(self, command_prefix, dict_list, dict_names_list, dir_prefix))
    await client.add_cog(ds.DictSpeak(client, '!', dict_list, dict_names_list, 'dictionaries/'))
    await client.add_cog(bk.BookKeeper(client))
import asyncio
asyncio.run(main())

# token = input('Please type in the Discord token: ')
token = None
with open(".env") as f:
    line = f.read()
    tokens = line.split("=")
    token = tokens[1]
client.run(token)
