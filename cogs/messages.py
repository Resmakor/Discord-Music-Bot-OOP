import discord
from discord.ext import commands
import validators
import asyncio

class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot_prefix = client.command_prefix
      
    @commands.Cog.listener()
    async def on_ready(self):
        """Function changes bot status to: listening Young Leosia - Szklanki when bot is online"""
        print("Understandek is online")
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Young Leosia - Szklanki"))

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
                      
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Bot disconnects after 60 seconds of being silent"""
      if not member.id == self.client.user.id:
          return
      
      elif before.channel is not None:
          return
      
      else:
          voice = after.channel.guild.voice_client
          while True:
              await asyncio.sleep(60)
              if voice.is_playing() == False and voice.is_paused() == False:
                  await voice.disconnect()
                  break    

def setup(client):
    client.add_cog(Messages(client))
