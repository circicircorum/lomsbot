import discord
from discord.ext import commands

import cogs.dictspeak as ds
import cogs.bookkeeper as bk
import cogs.pickergame as pg

class LOMS(commands.Bot):
    """
    LOMS.
    """


    def __init__(self, dict_list, dict_names_list, command_prefix=['!'], picker_param=0.8, description='LOMS.'):
        # initialise bot
        super().__init__(command_prefix=command_prefix, description=description, help_command=None)

        # add a prefix to all entries in the dictionary list
        dir_prefix = 'dictionaries/'

        # add cogs
        self.add_cog(ds.DictSpeak(self, command_prefix, dict_list, dict_names_list, dir_prefix))
        self.add_cog(bk.BookKeeper(self))
        self.add_cog(pg.PickerGame(self, 'padoru token', 'https://cdn.discordapp.com/attachments/655083242587684874/785739068980985886/781002161550917672.png', picker_param))


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
    
