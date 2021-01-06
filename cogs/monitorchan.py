import discord
from discord.ext import commands

class MonitorChan(commands.Cog):
    """
    Monitors channels.
    """

    def __init__(self, bot, channel_id=SECRET_CHANNEL_ID):
        self.bot = bot
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.bot.get_channel(self.cid)
        
        if self.channel is None:
            print("Error: self.channel is None.")
            raise


    @commands.group()
    async def react(self, ctx):
        if self.channel is None:
            return await ctx.send('Please wait for the bot to be ready (channel not found).')
        
        guild_roles = self.bot.get_guild(SECRET_SERVER_ID).roles
        if guild_roles is None:
            return await ctx.send('Please wait for the bot to be ready (guild not found).')
        
        if guild_roles[-1] not in ctx.message.author.roles:
            return await ctx.send('Please obtain the necessary permissions to add reaction images.')
        pass


    @react.command(name='upload')
    async def __upload_image(self, ctx, file_type, reaction_name, link):

        # download file using the link provided
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                if resp.status != 200:
                    return await ctx.send('Error while downloading file.')
                data = io.BytesIO(await resp.read())

                # upload file to specified channel
                rfile = discord.File(data)
                rfile.filename = reaction_name + '.' + file_type
                message = await self.channel.send(content=reaction_name, file=rfile)

        if message is None:
            return await ctx.send('Error while retrieving image message.')
    

    @react.command(name='add')
    async def __upload_image(self, ctx, reaction_name, link):
        
        # download file using the link provided
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                if resp.status != 200:
                    return await ctx.send('Error while downloading file.')
                data = io.BytesIO(await resp.read())


                rfile = discord.File(data)
                rfile.filename = reaction_name + '.' + file_type
                message = await self.channel.send(content=reaction_name, file=rfile)
