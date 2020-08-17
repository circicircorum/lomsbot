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
        channel = self.get_channel(730386849570357258)
        await channel.send(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(message, end='\n\n')
        
        print('Message from {0.author}: {0.content}'.format(message), end='\n\n')

        # message.content is a single string(?)
        if False:
            print(dir(message))

        if message.content[0] == '!':
            await self.process_command(message)

    async def process_command(self, message):
        msg_tokens = message.content.split()
        if msg_tokens[0] == '!test':
            await message.channel.send("Testing command...")
        elif msg_tokens[0] == '!wah':
            await message.channel.send('<:migu:740390882435530792>')
        elif msg_tokens[0] == '!fish':
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
