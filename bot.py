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
        elif msg_tokens[0] == '!concern':
            await message.channel.send('https://cdn.discordapp.com/attachments/658813940268269668/744772320282935326/image0-12.jpg')
        elif msg_tokens[0] == '!jail':
            await message.channel.send('https://cdn.discordapp.com/attachments/658813940268269668/744772320043728918/go_to_horny_jail_bonk.jpg')
        elif msg_tokens[0] == '!heh':
            await message.channel.send('https://cdn.discordapp.com/attachments/658813940268269668/743890032665952286/tsubasa_chibi_bliss_cutout.png')
            


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
