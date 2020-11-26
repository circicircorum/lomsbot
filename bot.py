import discord
from discord.ext import commands
import os
import sys
from dotenv import load_dotenv
import logging


import cogs.dictspeak as ds
import cogs.monitorchan as mc
import cogs.bookkeeper as bk


class LOMS(commands.Bot):
    '''
    class LOMS(commands.Bot)

    LOMS.
    '''


    def __init__(self, command_prefix=['!'], description='LOMS.'):
        # initialise bot
        super().__init__(command_prefix=command_prefix, description=description, help_command=None)

        # names dictionaries containing simple "commands"
        dict_list =         ['img_dict.json',   'img2_dict.json',   'special_dict.json',    'info_dict.json']
        dict_names_list =   ['images',          'images-2',         'special',              'info']

        # add a prefix to all entries in the dictionary list
        dir_prefix = 'dictionaries/'
        for index, filename in enumerate(dict_list):
            dict_list[index] = dir_prefix + filename

        # add cogs
        self.add_cog(ds.DictSpeak(self, command_prefix, dict_list, dict_names_list))
        self.add_cog(mc.MonitorChan(self))
        self.add_cog(bk.BookKeeper(self))


    async def on_ready(self):
        # send a message on the specified channel whenever the bot becomes ready
        print(f'Logged on as {self.user}!')
        channel = self.get_channel(730386849570357258)
        await channel.send(f'Logged on as {self.user}!')


    async def on_message(self, message):
        # log all messages with their attributes to standard output
        print(message, end='\n\n')
        print('Message from {0.author}: {0.content}'.format(message), end='\n\n')

        # invoke default method
        await self.process_commands(message)
    


# define main function
def main():
    # load environment variables
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # set up logging
    logging.basicConfig(level=logging.INFO)

    # instantiate bot
    if len(sys.argv) > 1:
        bot = LOMS(sys.argv[1])
    else:
        bot = LOMS()

    # run bot
    bot.run(TOKEN)


# run main()
if __name__ == "__main__":
    main()
