import discord
from discord.ext import commands, tasks
import random
import time
import datetime
import math
from collections import defaultdict

class PickerGame(commands.Cog):
    '''
    class PickerGame(commands.Cog)

    A simple game where players pick up tokens.
    '''


    def __init__(self, bot, token_name, token_img_link, param=1.0):
        self.bot = bot
        self.token_name = token_name
        self.token_img_link = token_img_link
        self.param = float(param)
        
        # track the number of tokens currently in a channel
        self.token_count_by_channel = defaultdict(int)

        # track the number of tokens held by a user
        self.token_count_by_user = defaultdict(int)

        # list of messages by channel ID
        self.message_buffer = defaultdict(list)
        
        # list of channels to exclude
        self.channel_exclusion_list = [777782490525335582, 655083022294581278, 680690289928699904,
                                       748129827910844456, 655041534873436161, 757398739223576646]
        
        # ID of the participating guild
        self.EVENT_GUILD_ID = 620170948708007937
    

    @commands.Cog.listener()
    async def on_ready(self):
        self.drop_token.start()

    
    async def __drop_token(self):
        # loop until an appropriate channel is chosen
        while True:
            channel = random.choice(self.bot.get_guild(self.EVENT_GUILD_ID).channels)
            if channel.id not in self.channel_exclusion_list and channel.type == discord.ChannelType['text']:
                if channel.permissions_for(self.bot.get_guild(self.EVENT_GUILD_ID).get_member(self.bot.user.id)).send_messages:
                    break
                #else:
                #    print("\nBot does not have the required permissions to send a token in the channel with ID %d.\n" % channel.id)
        
        # increment the token count of the channel
        self.token_count_by_channel[str(channel.id)] += 1

        # send token drop message
        desc_txt = 'Hey, look! It\'s a ' + self.token_name + '!\n'
        message = await channel.send(embed=discord.Embed(description=desc_txt).set_image(url=self.token_img_link))
        
        # store message in message buffer 
        self.message_buffer[str(channel.id)].append(message)
        #except:
            #print('\nError occurred while trying to drop a token in channel ' + str(channel.id) + '\n')


    @tasks.loop()
    async def drop_token(self):
        await self.__drop_token()

        # set next token drop time
        delta = -math.log(random.random()) / self.param * 1000
        self.drop_token.change_interval(seconds=delta)
        print('\nNext token drops in: ' + str(delta) + '\n')


    @commands.command(name='pick')
    async def pick_token(self, ctx):
        if self.token_count_by_channel[str(ctx.message.channel.id)] > 0:
            self.token_count_by_channel[str(ctx.message.channel.id)] -= 1
            self.token_count_by_user[ctx.message.author.id] += 1

            await ctx.send(ctx.message.author.mention + ' picked up a ' + self.token_name + '!')
            await self.message_buffer[str(ctx.message.channel.id)][-1].delete()
            await ctx.message.delete()

        else:
            await ctx.send('There are no tokens to be picked in this channel. Please wait for a ' + self.token_name + ' to spawn.')
    

    @commands.command(name='drop')
    async def force_drop_token(self, ctx):
        if self.bot.get_guild(self.EVENT_GUILD_ID).roles[-1] not in ctx.message.author.roles:
            return await ctx.send('Please obtain the necessary permissions to drop tokens.')
        await self.__drop_token()
    

    @commands.command(name='leaderboard')
    async def check_token_leaderboard(self, ctx):
        message_text = 'Leaderboard: ```\n'

        # iterate through the dictionary
        for user_id, token_count in sorted(self.token_count_by_user.items()):
            
            user = self.bot.get_user(user_id)

            # check if user exists
            if user is not None:
                message_text += '%s: %s\n' % (user.display_name, str(token_count))
        
        message_text += '```'
        
        await ctx.send(message_text)

