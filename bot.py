import discord
#import psycopg2
import os
import json
from dotenv import load_dotenv

from commands import *
import constants


# load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_URL = os.getenv('DATABASE_URL')


class LOMS(discord.Client):
    '''
    LOMS()

    LOMS.
    '''

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = self.get_channel(730386849570357258)
        await channel.send(f'Logged on as {self.user}!')

        self.command_dict = {
            'test'          :   Command('Test Command'),
            'invite'        :   SendMessageCommand('Send Invite', message_text='Click the link below to invite LOMSBot:\nhttps://discord.com/oauth2/authorize?client_id=730301823512215563&scope=bot&permissions=1'),
            #'fish'      :   SendMessageCommand('Fish',          message_text='https://cdn.discordapp.com/emojis/651604101226037274.gif?v=1',
            #                                                    description='Fish.'),
            'list-images'   :   SendFormattedMessageCommand('List Images', message_type=constants.LIST_IMAGES_COMMAND, dictionary=self.img_dict)
        }
        self.command_dict['commands'] = SendFormattedMessageCommand('List Commands', message_type=constants.LIST_COMMANDS_COMMAND, dictionary=self.command_dict)
    

    async def on_message(self, message):
        print(message, end='\n\n')
        print('Message from {0.author}: {0.content}'.format(message), end='\n\n')

        if message.content[0] == '!':
            await self.process_command(message)


    async def process_command(self, message):
        msg_tokens = message.content.split()

        if msg_tokens[0][1:] in self.command_dict.keys():
            await self.command_dict[msg_tokens[0][1:]].action(discord_message=message)
        elif msg_tokens[0][1:] in self.img_dict.keys():
            await message.channel.send(self.img_dict[msg_tokens[0][1:]])
    

    def init_dict(self, filename):
        with open('img_dict.json', 'r') as f:
            self.img_dict = json.load(f)
        
        for key, value in self.img_dict.items():
            if isinstance(value, list):
                self.img_dict[key] = ' '.join(value)


# define main function
def main():
    # instantiate bot
    client = LOMS()

    # set up image dict
    client.init_dict(".txt")

    # run bot
    client.run(TOKEN)

# run main()
if __name__ == "__main__":
    main()
