from nextcord.ext import commands

class Connecting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def join(self, ctx):
        """Bot joins voice channel"""
        try:
            if not ctx.guild.voice_client in self.client.voice_clients:
                    channel = ctx.author.voice.channel
                    await channel.connect()
            else:
                await ctx.channel.send('I am in the voice channel!')
        except:
            await ctx.channel.send('You are not in the voice channel!')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dc(self, ctx):
        """Bot disconnects from voice channel"""
        if ctx.guild.voice_client in self.client.voice_clients:
            await ctx.send('See you soon!', tts=True, delete_after=4)
            await ctx.voice_client.disconnect()
        else:
            await ctx.channel.send('I am not in the voice channel!')

def setup(client):
    client.add_cog(Connecting(client))
