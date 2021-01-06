import discord
from discord.ext import commands, tasks
import random
import time
import datetime
import math
import json
from collections import defaultdict

class PickerGame(commands.Cog):
    """
    A simple game where players pick up tokens.
    """


    def __init__(self, bot, token_name, token_img_link, param=10.0, game_file_dir_prefix='picker/', load_game_files=False):

        self.bot = bot
        self.token_name = token_name
        self.token_img_link = token_img_link
        self.game_file_dir_prefix = game_file_dir_prefix
        self.param = float(param)

        self.init_game()
        self.init_shop(load_game_files)
    
    
    def init_game(self):
        # track the number of tokens currently in a channel
        self.token_count_by_channel = defaultdict(int)

        # track the number of tokens held by a user
        self.token_count_by_user = defaultdict(int)

        # list of messages by channel ID
        self.message_buffer = defaultdict(list)
        
        # list of channels to exclude
        self.channel_exclusion_list = [777782490525335582, 655083022294581278, 680690289928699904,
                                       748129827910844456, 655041534873436161, 757398739223576646,
                                       757195732192067594, 655095573229338644, 655829744075538432,
                                       676018759319945246]
        
        # ID of the participating guild
        self.EVENT_GUILD_ID = 620170948708007937
    

    def init_shop(self, load=False):
        self.item_list_by_user = {}
        self.item_value_list = defaultdict(int)

        if load:
            with open(self.game_file_dir_prefix + 'pickergame.json', 'r', encoding='utf-8') as f:
                self.item_value_list = json.load(f)['items']
        else:
            self.item_value_list['apple'] = 1
            self.item_value_list['share'] = 5
            self.item_value_list['coin'] = 10
    
    
    async def __drop_token(self):
        # loop until an appropriate channel is chosen
        while True:
            channel = random.choice(self.bot.get_guild(self.EVENT_GUILD_ID).channels)
            if channel.id not in self.channel_exclusion_list and channel.type == discord.ChannelType['text']:
                if channel.permissions_for(self.bot.get_guild(self.EVENT_GUILD_ID).get_member(self.bot.user.id)).send_messages:
                    break

        # increment the token count of the channel
        self.token_count_by_channel[str(channel.id)] += 1

        # send token drop message
        desc_txt = 'Hey, look! It\'s a ' + self.token_name + '!\n'
        message = await channel.send(embed=discord.Embed(description=desc_txt).set_image(url=self.token_img_link))
        
        # store message in message buffer
        self.message_buffer[str(channel.id)].append(message)


    @tasks.loop()
    async def drop_token(self):
        await self.__drop_token()

        # set next token drop time
        delta = -math.log(random.random()) / self.param * 1000
        self.drop_token.change_interval(seconds=delta)
        print('\nToken drop interval changed to: ' + str(delta) + '\n')


    @commands.command(name='pick')
    async def pick_token(self, ctx):
        try:
            if self.token_count_by_channel[str(ctx.message.channel.id)] > 0:
                self.token_count_by_channel[str(ctx.message.channel.id)] -= 1
                self.token_count_by_user[ctx.message.author.id] += 1
            
                message = await ctx.send(ctx.message.author.mention + ' picked up a ' + self.token_name + '!')
                await self.message_buffer[str(ctx.message.channel.id)][-1].delete()
                await ctx.message.delete()
                await message.delete()

            else:
                message = await ctx.send('There are no tokens to be picked in this channel. Please wait for a ' + self.token_name + ' to spawn.')
                time.sleep(1)
                await ctx.message.delete()
                await message.delete()
        except:
            print('Exception raised in pick_token().\n')
    

    @commands.command(name='drop')
    async def force_drop_token(self, ctx):
        if self.bot.get_guild(self.EVENT_GUILD_ID).roles[-1] not in ctx.message.author.roles:
            return await ctx.send('Please obtain the necessary permissions to drop tokens.')
        await self.__drop_token()


    @commands.command(name='drophere')
    async def force_drop_token_here(self, ctx):
        if self.bot.get_guild(self.EVENT_GUILD_ID).roles[-1] not in ctx.message.author.roles:
            return await ctx.send('Please obtain the necessary permissions to drop tokens.')
        
        # check if an appropriate channel was chosen
        channel = ctx.message.channel
        if channel.id in self.channel_exclusion_list or not channel.permissions_for(self.bot.get_guild(self.EVENT_GUILD_ID).get_member(self.bot.user.id)).send_messages:
            return

        # increment the token count of the channel
        self.token_count_by_channel[str(channel.id)] += 1

        # send token drop message
        desc_txt = 'Hey, look! It\'s a ' + self.token_name + '!\n'
        message = await channel.send(embed=discord.Embed(description=desc_txt).set_image(url=self.token_img_link))
        
        # store message in message buffer
        self.message_buffer[str(channel.id)].append(message)
    

    @commands.command(name='give')
    async def give_token(self, ctx, user, count):
        if self.bot.get_guild(self.EVENT_GUILD_ID).roles[-1] not in ctx.message.author.roles:
            return await ctx.send('Please obtain the necessary permissions to give tokens.')
        
        # strip pings down to the user id and check that the input is valid
        try:
            user_id = str(user.strip('<@!>'))
            count = int(count)
            self.token_count_by_user[user_id] += count
        except ValueError:
            print('ValueError in give_token().\n')
            return

        # send an acknowledgement message
        if count >= 0:
            message = await ctx.send(user + ' was given ' + str(count) + ' ' + self.token_name + '(s)!')
        elif count < 0:
            message = await ctx.send(user + ' had ' + str(-count) + ' of their ' + self.token_name + '(s) taken away!')
        
        # delete the messages after some time
        time.sleep(1)
        await ctx.message.delete()
        await message.delete()
    

    @commands.command(name='leaderboard')
    async def check_token_leaderboard(self, ctx):
        message_text = 'Leaderboard: ```\n'

        # iterate through the dictionary
        for user_id, token_count in sorted(self.token_count_by_user.items(), key=lambda x : x[1], reverse=True):
            
            user = self.bot.get_user(int(user_id))

            # check if user exists
            if user is not None:
                message_text += '%s: %s\n' % (user.display_name, str(token_count))
        
        message_text += '```'
        
        await ctx.send(message_text)


    @commands.group()
    async def shop(self, ctx):
        pass


    @shop.command(name='list')
    async def list_shop_item(self, ctx, sort=''):
        # sort entries as required
        if sort == 'name':
            entries = sorted(self.item_value_list.items(), key=lambda item: item[0])
        elif sort == 'value':
            entries = sorted(self.item_value_list.items(), key=lambda item: item[1])
        else:
            entries = self.item_value_list.items()

        sorted_entries = [item_name + ': ' + str(item_value) for item_name, item_value in entries]
        sorted_entries = '\n'.join(sorted_entries)
        await ctx.send('List of items: \n```\n'
                        + sorted_entries
                        + '```')
    

    @commands.command(name='inventory')
    async def list_inventory(self, ctx, sort=''):
        user_id = str(ctx.message.author.id)
        
        try:
            # sort entries as required
            if sort == 'name':
                entries = sorted(self.item_list_by_user[user_id].items(), key=lambda item: item[0])
            elif sort == 'value':
                entries = sorted(self.item_list_by_user[user_id].items(), key=lambda item: self.item_value_list[item[0]])
            else:
                entries = self.item_list_by_user[user_id].items()

            sorted_entries = [item_name + ': ' + str(item_value) for item_name, item_value in entries]
            sorted_entries = '\n'.join(sorted_entries)
            await ctx.send('Account balance: ' + str(self.token_count_by_user[user_id]) + '\n'
                            + 'List of items: \n```\n'
                            + sorted_entries
                            + '```')
        except KeyError:
            self.item_list_by_user[user_id] = defaultdict(int)
            await ctx.send('Account balance: ' + str(self.token_count_by_user[user_id]) + '\n'
                            + 'No items held.')


    @shop.command(name='buy')
    async def buy_item(self, ctx, item_name, amount=1):
        user_id = str(ctx.message.author.id)

        if item_name not in self.item_value_list.keys():
            return await ctx.send('Invalid item name.')
        if amount == 0:
            return
        if amount < 0:
            return await ctx.send('To sell items, please use ``shop sell [name of item] [amount]``.')

        # check payment
        if self.token_count_by_user[user_id] < self.item_value_list[item_name] * amount:
            return await ctx.send('You have insufficent funds to complete the purchase.')
        self.token_count_by_user[user_id] -= self.item_value_list[item_name] * amount
        
        # give item
        try:
            self.item_list_by_user[user_id][item_name] += amount
        except KeyError:
            self.item_list_by_user[user_id] = defaultdict(int)
            self.item_list_by_user[user_id][item_name] += amount
        
        await ctx.send('Bought ' + item_name + '!')


    @shop.command(name='sell')
    async def sell_item(self, ctx, item_name, amount=1):
        user_id = str(ctx.message.author.id)

        if item_name not in self.item_value_list.keys():
            return await ctx.send('Invalid item name.')
        if amount == 0:
            return
        if amount < 0:
            return await ctx.send('To buy items, please use ``shop buy [name of item] [amount]``.')

        # check item
        try:
            if self.item_list_by_user[user_id][item_name] < amount:
                return await ctx.send('You do not have enough of the item to sell.')
            self.item_list_by_user[user_id][item_name] -= amount
        except KeyError:
            return await ctx.send('You do not have enough of the item to sell.')
        
        # pay user
        self.token_count_by_user[user_id] += self.item_value_list[item_name] * amount
        
        await ctx.send('Sold ' + item_name + '!')


    @commands.group()
    @commands.is_owner()
    async def game(self, ctx):
        pass


    @game.command(name='save')
    async def save_leaderboard(self, ctx):
        with open(self.game_file_dir_prefix + 'picker-game-leaderboard.json', 'w', encoding='utf-8') as f:
            json.dump(self.token_count_by_user, f, indent=4)
        with open(self.game_file_dir_prefix + 'picker-game-user-items.json', 'w', encoding='utf-8') as f:
            json.dump(self.item_list_by_user, f, indent=4)
        await ctx.send('Saved game stats to file.')


    @game.command(name='load')
    async def load_leaderboard(self, ctx):
        with open(self.game_file_dir_prefix + 'picker-game-leaderboard.json', 'r', encoding='utf-8') as f:
            self.token_count_by_user = json.load(f)
        with open(self.game_file_dir_prefix + 'picker-game-user-items.json', 'r', encoding='utf-8') as f:
            self.item_list_by_user = json.load(f)
        await ctx.send('Loaded game stats from file.')


    @game.command(name='commence')
    async def start_picker_game(self, ctx, param=None):
        if hasattr(self, 'game_ongoing') and self.game_ongoing:
            return await ctx.send('There is already an ongoing Game.')
        
        try:
            self.param = float(param)
        except:
            pass

        await ctx.send('Let the Games begin!')
        self.game_ongoing = True
        self.drop_token.start()


    @game.command(name='end')
    async def end_picker_game(self, ctx):
        if not hasattr(self, 'game_ongoing') or not self.game_ongoing:
            return await ctx.send('There are no ongoing Games currently.')
        
        await ctx.send('The Games have ended!')
        self.game_ongoing = False
        self.drop_token.cancel()


    @game.command(name='reset')
    async def reset_picker_game(self, ctx):
        await ctx.send('Resetting the Game!')

        # reset game parameters
        self.init_game()


    @game.command(name='param')
    async def peek_param(self, ctx):
        await ctx.send('lambda: ' + str(self.param))
