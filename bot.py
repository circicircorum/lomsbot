import discord

import os
from dotenv import load_dotenv

# load DISCORD_TOKEN
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class LOMS(discord.Client):
    '''
    LOMS()

    LOMS.
    '''

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(message, end='\n\n')
        
        print('Message from {0.author}: {0.content}'.format(message), end='\n\n')

        # message.content is a single string(?)
        if False:
            print(dir(message))

        if message.content[0] == '!':
            await self.process_command(message)

    async def process_command(self, message):
        vid_url = 'https://www.youtube.com/watch?v=tU8FZtkTqos'
        test_emb = discord.Embed(title='embed_message', url=vid_url)
        msg_tokens = message.content.split()
        if msg_tokens[0] == '!test':
            await message.channel.send("Testing command...")
        elif msg_tokens[0] == '!testmore':
            await message.channel.send('Testing file...', file=discord.File('res/test.txt'), embed=test_emb)
        elif msg_tokens[0] == '!embed':
            await message.channel.send("Testing embed...", embed=test_emb)
        elif msg_tokens[0] == '!file':
            await message.channel.send('Testing file...', file=discord.File('res/test.txt'))
        elif msg_tokens[0] == '!img':
            await message.channel.send('Testing image...', file=discord.File('res/test.png'))
        elif msg_tokens[0] == '!wah':
            await message.channel.send('<:migu:740390882435530792>')
        elif msg_tokens[0] == '!smile':
            await message.channel.send(file=discord.File('res/336656661387411456.png'))
        elif msg_tokens[0] == '!fish':
            #fish_emb = discord.Embed(url='https://cdn.discordapp.com/emojis/651604101226037274.gif?v=1')
            #fish_emb = discord.Embed(height=10, width=10)
            #fish_emb.set_image(url='https://cdn.discordapp.com/emojis/651604101226037274.gif?v=1')
            #print(fish_emb.image)
            #await message.channel.send(embed=fish_emb)
            await message.channel.send('https://cdn.discordapp.com/emojis/651604101226037274.gif?v=1')


# define main function
def main():
    # instantiate bot
    #client = discord.Client()
    client = LOMS()

    # run bot
    client.run(TOKEN)

# run main()
if __name__ == "__main__":
    main()
