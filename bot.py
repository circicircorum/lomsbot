import discord
from discord.ext import commands
import logging
import os
from dotenv import load_dotenv

import cogs


class LOMS(commands.Bot):
    '''
    LOMS()

    LOMS.
    '''
    def __init__(self, command_prefix='?', description='LOMS.'):
        # initialise bot
        super().__init__(command_prefix=command_prefix, description=description)

        # add cogs
        self.add_cog(cogs.DictSpeak(self, command_prefix, ['img_dict.json', 'info_dict.json'], ['images', 'info']))
        #self.add_cog(cogs.Bookkeeper(self))

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = self.get_channel(730386849570357258)
        await channel.send(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(message, end='\n\n')
        print('Message from {0.author}: {0.content}'.format(message), end='\n\n')
        await self.process_commands(message)


# define main function
def main():
    # load environment variables
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # set up logging
    logging.basicConfig(level=logging.INFO)

    # instantiate bot
    bot = LOMS()

    # run bot
    bot.run(TOKEN)

# run main()
if __name__ == "__main__":
    main()
