import discord
from discord.ext import commands
from random import choice
from os import environ


class Accessories(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot_prefix = client.command_prefix
        self.bot_id = int(environ['bot_id'])

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def listen(self, ctx, member : discord.Member):
        """Function send messages with some details about discord member who's listening to song on Spotify"""
        try:
            sname = member.activity.title
            sartists = member.activity.artists
            album = member.activity.album
            palbum = member.activity.album_cover_url
            duration = str(member.activity.duration)[:-7].strip()
            quick_embed = discord.Embed(title=f"{member} listens now {sname} from album {album}, there are artists such as: {sartists}", description=f'Song duration **{duration}**', colour=0xeb1e1e)
            quick_embed.set_thumbnail(url=palbum)
            await ctx.channel.send(embed=quick_embed)
        except:
            await ctx.channel.send("Can't hear anything!")

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def clear(self, ctx, amount):
        """Bot clears text channel by deleting its own messages and messages with bot prefix"""
        try:
            amount = abs(int(amount))
        except:
            await ctx.channel.send(f"Argument '{amount}' is not a valid argument!")
            return
        if amount > 150:
            await ctx.channel.send(f"{amount} is too much for me! Cleaning 150 messages...", delete_after=5)
            amount = 150
        deleted_messages = await ctx.channel.purge(limit=amount, check=lambda x: self.bot_prefix in x.content or self.bot_id == x.author.id)
        how_many = len(deleted_messages)
        await ctx.send(f"**{how_many}** messages have been deleted! ♻️", delete_after=10)

    @commands.command()
    async def coin(self, ctx):
        """Function tosses a coin"""
        to_be_drawn = ('Heads', 'Tails')
        await ctx.channel.send(choice(to_be_drawn))

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cannon(self, ctx, member : discord.Member):
        """Bot is moving specific user through all channels. Afterwards user is back on his previous channel"""
        try:
            if member.bot:
                await ctx.channel.send("Sam sie wysadz ;PP")
                return
            cannon = nextcord.utils.find(lambda r: r.name == 'cannon', ctx.message.guild.roles)
        except:
            await ctx.channel.send('Could not find role cannon on the server!')
            return
        if cannon in ctx.author.roles:
            try:
                current_channel_id = member.voice.channel.id
                voice_channels = ctx.guild.voice_channels
                voice_channels_ids = [channel.id for channel in voice_channels]
                if len(voice_channels_ids) > 8:
                    final_count = len(voice_channels_ids) - 7
                    voice_channels_ids = voice_channels_ids[:-final_count]
                if voice_channels_ids[-1] != current_channel_id:
                    voice_channels_ids.append(current_channel_id)
                for channel_id in voice_channels_ids:
                    channel = self.client.get_channel(channel_id)
                    await member.move_to(channel)
                gif_embed = nextcord.Embed(title="KABOOM!")
                gif_embed.set_image(url="https://c.tenor.com/u8jwYAiT_DgAAAAC/boom-bomb.gif")
                await ctx.channel.send(f'{member.mention} has been blown up!', embed=gif_embed)
            except Exception as e:
                await ctx.channel.send(f'{e}')
        else:
            await ctx.channel.send('You do not have sufficient permissions!')

def setup(client):
    client.add_cog(Accessories(client))
