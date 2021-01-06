import discord
from discord.ext import commands
import random

class BookKeeper(commands.Cog):
    """
    Contains some basic commands.
    """    


    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def invite(self, ctx):
        await ctx.send( 'Click the link below to invite LOMSBot:\n'
                        'https://discord.com/oauth2/authorize?client_id=730301823512215563&scope=bot&permissions=1')
    

    @commands.command(name='commands')
    async def command_list(self, ctx, sort=None):
        entries = [command.name for command in self.bot.commands]

        if sort == "sort":
            entries.sort()

        entries = '\n'.join(entries)
        await ctx.send('List of commands: \n```\n'
                            + entries
                            + '```')
    

    @commands.command(name='impostor')
    async def impostor_check(self, ctx, username):
        # define text length
        target_len = 40
        planet_symbols = '        •.。　ﾟ'
        lines = ['', '', '']
        app_len = [0, 0, 0]

        impostor_text = username + random.choice([' was not the impostor •. ඞ　', ' was the impostor •. ඞ　.'])
        
        # calculate padding for the middle line
        app_len[1] = len(impostor_text) + 1
        mid_padding = target_len - app_len[1]
        if mid_padding < 1:
            mid_padding = [0, 0]
        else:
            mid_padding = [round(mid_padding / 2), int(mid_padding / 2)]

        # generate lines and characters for padding
        for line_index in range(len(lines)):
            while app_len[line_index] < target_len:
                
                # append a random symbol to the line
                symbol_index = random.randrange(len(planet_symbols))
                symbol = planet_symbols[symbol_index]
                lines[line_index] += symbol

                # increment apparent length accordingly
                if symbol == '。' or symbol == '　ﾟ':
                    app_len[line_index] += 2
                else:
                    app_len[line_index] += 1
        
        # generate the middle line
        lines[1] = lines[1][:mid_padding[0]] + impostor_text + lines[1][mid_padding[0]:-1]
        
        
        await ctx.send('```\n' + '\n'.join([line for line in lines]) + '```')

        
        '''
        text = ['```。　　　　•　 　ﾟ　　。 　　.　　　.　　。 　　.　 　　　\n',
                '。　 .  They were not the impostor •. 。ඞ　.\n',
                '.　　　　　。　　 。　. 　.　 。。 　•   •　.```']

                #        "```。　　　　•　 　ﾟ　　。 　　.　　　.　　。 　　.　 　　　\n。　 . • • They were the impostor •. 。ඞ　.\n.　　　　　。　　 。　. 　.　 。。 　•   •　.```"],
        '''