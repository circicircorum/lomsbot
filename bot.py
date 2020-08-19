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

        self.img_dict = {}

    async def on_message(self, message):
        print(message, end='\n\n')
        print('Message from {0.author}: {0.content}'.format(message), end='\n\n')


        if message.content[0] == '!':
            await self.process_command(message)

    async def process_command(self, message):
        msg_tokens = message.content.split()

        if msg_tokens[0] == '!test':
            await message.channel.send("Testing command...")
        elif msg_tokens[0] == '!invite':
            await message.channel.send("Click the link below to invite LOMSBot:\nhttps://discord.com/oauth2/authorize?client_id=730301823512215563&scope=bot&permissions=1")
        elif msg_tokens[0] == '!list':
            await message.channel.send('• List of reaction images:\n```\n' 
                                        + '\n'.join(self.img_dict.keys())
                                        + '```'
                                        + '\nExample: \n'
                                        + '```!fish```')
        elif msg_tokens[0][1:] in self.img_dict.keys():
            await message.channel.send(self.img_dict[msg_tokens[0][1:]])
        elif msg_tokens[0] == '!jar':
            await message.channel.send()

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
