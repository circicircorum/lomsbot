
import discord
from discord.ext import commands

class BookKeeper(commands.Cog):
    '''
    class BookKeeper(commands.Cog)

    For some basic commands.
    '''


    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def invite(self, ctx):
        await ctx.send( 'Click the link below to invite LOMSBot:\n'
                        'https://discord.com/oauth2/authorize?client_id=730301823512215563&scope=bot&permissions=1')
    
    @commands.command(name='commands')
    async def command_list(self, ctx):
        await ctx.send('List of commands: \n```\n'
                            + '\n'.join([command.name for command in self.bot.commands])
                            + '```')