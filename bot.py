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

        self.img_dict = {'wah'      :   '<:migu:740390882435530792>',
                         'fish'     :   'https://cdn.discordapp.com/emojis/651604101226037274.gif?v=1',
                         'concern'  :   'https://cdn.discordapp.com/attachments/658813940268269668/744914783660408904/image0-12.jpg',
                         'jail'     :   'https://cdn.discordapp.com/attachments/658813940268269668/744914783320539166/go_to_horny_jail_bonk.jpg',
                         'heh'      :   'https://cdn.discordapp.com/attachments/658813940268269668/743890032665952286/tsubasa_chibi_bliss_cutout.png'}


    async def on_message(self, message):
        print(message, end='\n\n')
        print('Message from {0.author}: {0.content}'.format(message), end='\n\n')


        if message.content[0] == '!':
            await self.process_command(message)

    async def process_command(self, message):
        msg_tokens = message.content.split()

        if msg_tokens[0] == '!test':
            await message.channel.send("Testing command...")
        elif msg_tokens[0] == '!list':
            await message.channel.send('• List of reaction images:\n```\n' 
                                        + '\n'.join(self.img_dict.keys())
                                        + '```'
                                        + '\nExample: \n'
                                        + '```!fish```')
        elif msg_tokens[0][1:] in self.img_dict.keys():
            await message.channel.send(self.img_dict[msg_tokens[0][1:]])
        elif msg_tokens[0] == '!jar':
            await message.channel.send('https://media.discordapp.net/attachments/491156706043232257/741047359752110144/jar_1.png')
            await message.channel.send('https://media.discordapp.net/attachments/491156706043232257/741047360209289226/fubuki.gif')
            await message.channel.send('https://media.discordapp.net/attachments/491156706043232257/741047360926384482/jar_2.png')


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
