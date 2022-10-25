import nextcord
from nextcord.ext import commands
import validators

class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot_prefix = client.command_prefix

    @commands.Cog.listener()
    async def on_ready(self):
        """Function changes bot status to: listening Young Leosia - Szklanki when bot is online"""
        print("Understandek is online")
        await self.client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="Young Leosia - Szklanki"))

    @commands.Cog.listener()
    async def on_message(self, message):
        """Bot responds to keywords related to 'xD' emote"""
        if message.author.bot == False and message.content != str(self.bot_prefix) and not validators.url(message.content):
            special_words = ['xd', 'xD', 'XD', 'Xd']
            for word in special_words:
                if word in message.content:
                    if word == 'Xd':
                        await message.channel.send('Xd is not an emote!')
                    else:
                        await message.channel.send(f'Haha {word}')

def setup(client):
    client.add_cog(Messages(client))