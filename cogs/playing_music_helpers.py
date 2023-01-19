import discord
from discord.ext import commands
from discord.utils import get 


class Playing_music_helpers(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot_prefix = client.command_prefix

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pause(self, ctx):
        """Function pauses music"""
        voice = get(self.client.voice_clients, guild=ctx.guild)
        try:
            if voice.is_playing():
                voice.pause()
                await ctx.channel.send('Song **paused** ⏸️')
            else:
                await ctx.channel.send('Nothing is playing right now!')
        except:
            await ctx.channel.send('Nothing is playing right now!')
            
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def resume(self, ctx):
        """Function resumes song"""
        voice = get(self.client.voice_clients, guild=ctx.guild)
        try:
            if voice.is_paused() and ctx.guild.voice_client in self.client.voice_clients:
                await ctx.channel.send('Song **resumed** ⏯️')
                voice.resume()
            else:
                await ctx.channel.send('Nothing is paused right now!')
        except:
            await ctx.channel.send('Nothing is paused right now!')

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def skip(self, ctx):
        """Function skips song"""
        voice = get(self.client.voice_clients, guild=ctx.guild)
        try:
            if voice.is_playing() or voice.is_paused() and ctx.guild.voice_client in self.client.voice_clients:
                await ctx.channel.send('Song **skipped** ⏹️')
                voice.stop()
            else:
                await ctx.channel.send('Nothing is playing right now!')
        except:
            await ctx.channel.send('Nothing is playing right now!')

    @commands.command()
    async def help(self, ctx):
        """Function shows available comments with description"""
        embed = nextcord.Embed(title="Commands", url="https://github.com/Resmakor", description="powered by Resmakor", color=0xeb1e1e)
        embed.add_field(name=f"{self.bot_prefix}play <song name>", value="Bot turns the music on and joins voice channel. If something is being played, song is added to queue", inline=False)
        embed.add_field(name=f"{self.bot_prefix}pause", value="Bot pauses song", inline=False)
        embed.add_field(name=f"{self.bot_prefix}resume", value ="Bot resumes song", inline=False)
        embed.add_field(name=f"{self.bot_prefix}skip", value="Bot skips song", inline=False)
        embed.add_field(name=f"{self.bot_prefix}queue", value="Bot shows queue status", inline=False)
        embed.add_field(name=f"{self.bot_prefix}loop", value="Bot loops next song till someone uses 'loop' command again!", inline=False)
        embed.add_field(name=f"{self.bot_prefix}forward <value>", value="Bot rewinds the song by the 'value' seconds", inline=False)
        embed.add_field(name=f"{self.bot_prefix}join", value="Bot joins voice channel", inline=False)
        embed.add_field(name=f"{self.bot_prefix}dc", value="Bot leaves voice channel", inline=False)
        embed.add_field(name=f"{self.bot_prefix}coin", value="Bot toss a coin", inline=False)
        embed.add_field(name=f"{self.bot_prefix}cannon <discordmember>", value="User is being thrown to some specific channels", inline=False)
        embed.add_field(name=f"{self.bot_prefix}clear <value>", value="Bot deletes messages with commands and its own back <value> messages", inline=False)
        embed.add_field(name=f"{self.bot_prefix}listen <discordmember>", value="Bot sends what someone is listening to on Spotify", inline=False)
        embed.add_field(name=f"{self.bot_prefix}clearq", value="Bot clears the queue", inline=False)
        await ctx.send(embed=embed, delete_after=30)

def setup(client):
    client.add_cog(Playing_music_helpers(client))
