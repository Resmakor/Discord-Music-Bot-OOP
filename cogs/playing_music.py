import nextcord
from nextcord import FFmpegOpusAudio
from nextcord.ext import commands
from nextcord.utils import get

import asyncio
import validators
import re
import time
import datetime
from datetime import timedelta

from youtube_dl import YoutubeDL, utils
from pytube import Playlist
from music_helpers import Music_helpers






class Playing_music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.embed_queue = nextcord.Embed(title="Queue  🎵 🎵 🎵", url="https://github.com/Resmakor", color=0x44a6c0)
        self.if_loop = False
        self.music_queue = []
        self.current_ctx = None
        self.current_url = None
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'youtube_include_dash_manifest': False}

    
    def add_to_embed(self, video_title, url, duration):
        """Function adds song to global embed related to queue"""
        min_dur = timedelta(seconds=duration)
        value_to_be_given = f"Estimated time: {min_dur} " + url
        self.embed_queue.add_field(name=f"{video_title}", value=value_to_be_given, inline=False)

    async def show_status(self, ctx, video_title, duration, id, colour_id):
        """Function shows which song is being played and add reactions to some of them (beloved and disgusting)"""
        min_dur = timedelta(seconds=duration)
        quick_embed = nextcord.Embed(title=f"{video_title} 🎵", description=f'Song duration **{min_dur}**', color=colour_id)
        quick_embed.set_thumbnail(url=f"https://img.youtube.com/vi/{id}/0.jpg")
        await ctx.channel.send(embed=quick_embed)
        await self.client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=video_title))
        
        title_to_upper = video_title.upper()
        beloved = ['LEOSIA', 'SENTINO', 'POWW']
        disgusting = ['SZPAKU', 'CHIVAS']

        for word in beloved:
            if word in title_to_upper:
                await ctx.message.add_reaction("❤️")
                break

        for word in disgusting:
            if word in title_to_upper:
                await ctx.message.add_reaction("🥶")
                await ctx.message.add_reaction("🤮")
                await ctx.message.author.send("Reflect on yourself :)")
                break

    async def show_time(self, ctx, timer : str):
        """Function shows time of a song already set"""
        await ctx.channel.send(f'Current time set to: **{timer}**', delete_after=10)    

    def play_queue(self):
        """Function plays music in 'queue' order. When list of songs is empty playing is finished."""

        if len(self.music_queue) > 0:
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(self.music_queue[0]["song_url"], download=False)
                    video_title = info.get('title', None)
                    self.duration = info['duration']

            self.current_ctx = self.music_queue[0]["ctx"]
            self.current_url = self.music_queue[0]["song_url"]
            voice = get(self.client.voice_clients, guild=self.current_ctx.guild)
            self.started_time = 0

            URL = info['formats'][0]['url']
            ids = re.findall(r"watch\?v=(\S{11})", self.music_queue[0]['song_url'])
            id = ids[0]
            colour_id = Music_helpers.get_colour(id)

            if not voice.is_playing():
                voice.play(FFmpegOpusAudio(URL, **self.music_queue[0]["FFMPEG_OPTIONS"]), after = lambda e: self.play_queue())
                self.started_time = time.time()
            timer = self.music_queue[0]['FFMPEG_OPTIONS']['before_options'][4:15]
            
            if voice.is_playing():
                if '00:00:00.00' == timer:
                    self.client.loop.create_task(self.show_status(self.current_ctx, video_title, self.duration, id, colour_id))
                    self.previous_seconds = self.previous_minutes = self.previous_hours = 0
                else: 
                    self.client.loop.create_task(self.show_time(self.current_ctx, timer))
                if self.if_loop == False:
                    del self.music_queue[0]
                    self.embed_queue.remove_field(0)
                  
        else:
            self.current_ctx = None
            self.current_url = None

    def get_ss_time(self, seconds, end):
        """Function gets valid time after forward command (to change FFMPEG OPTIONS)"""
        """For instance: 00:01:20.00"""
        seconds = abs(seconds)
        print(self.duration)
        h = int(self.duration / 3600)
        m = int((self.duration / 60) % 60)
        s = self.duration % 60

        ss_music_whole_time = str(datetime.time(h, m, s)) + ".00"


        current_hours = int(round(end - self.started_time) / 3600)
        current_minutes = int(round(end - self.started_time) / 60)
        current_seconds = round(end - self.started_time) % 60

        new_hours = self.previous_hours + int(seconds / 3600) + current_hours
        new_minutes = self.previous_minutes + int(seconds / 60) + current_minutes
        new_seconds = self.previous_seconds + (seconds % 60) + current_seconds

        print("Time passed: ", current_hours, current_minutes, current_seconds)
        print("New time: ", new_hours, new_minutes, new_seconds)

        if new_seconds >= 60:
            new_minutes += int(new_seconds / 60)
            new_seconds = (new_seconds % 60)
            if new_minutes >= 60:
                new_hours += int(new_minutes / 60)
                new_minutes = new_minutes % 60

        elif new_minutes >= 60:
            new_hours += int(new_minutes / 60)
            new_minutes = new_minutes % 60

        ss_time = str(datetime.time(new_hours, new_minutes, new_seconds)) + ".00"
        print(ss_time)
        print(ss_music_whole_time)

        if ss_music_whole_time > ss_time:
            self.previous_hours = new_hours
            self.previous_minutes = new_minutes
            self.previous_seconds = new_seconds
            return ss_time
        else:
            return 0    

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.guild)
    async def forward(self, ctx, seconds):
        """Function rewinds the song by a given number of seconds"""
        try:
            seconds = int(seconds)
        except:
            await ctx.channel.send(f"Argument '{seconds}' is not a valid argument!")
            return   
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing() and ctx.guild.voice_client in self.client.voice_clients:
            end = time.time()
            ss_time = self.get_ss_time(seconds, end)
            if ss_time != 0 and self.if_loop == False:
                self.music_queue.insert(0, {"ctx" : self.current_ctx, "song_url" : self.current_url, "FFMPEG_OPTIONS" : {'before_options': f'-ss {ss_time} -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}})
            voice.stop()
        else:
            await ctx.channel.send("Nothing is playing right now!")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def loop(self, ctx):
        """Function starts loop"""
        """Loop makes it so that songs are no longer removed from the 'list_of_songs' and 'ctx_queue'"""
        if self.if_loop == False:
            self.if_loop = True
            await ctx.send("Loop **enabled** 🔁")
        else:
            self.if_loop = False
            await ctx.send("Loop **disabled** ❌")
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice.is_playing() and len(self.music_queue) > 0:
                    del self.music_queue[0]
                    self.embed_queue.remove_field(0)

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    async def queue(self, ctx):
        """Function shows status of queue"""
        await ctx.channel.send(embed=self.embed_queue, delete_after=30)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def clearq(self, ctx):
        """Function clears queue"""
        self.music_queue = []
        self.embed_queue = nextcord.Embed(title="Queue  🎵 🎵 🎵", url="https://github.com/Resmakor", color=0x44a6c0)
        await ctx.channel.send("Queue is empty!", delete_after=3)
  
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def play(self, ctx, url1 = "", url2 = "", url3 = "", url4 = "", url5 = "", url6 = ""):
        """Function deals with bot joining voice channel, getting valid YouTube url,"""
        """downloading YouTube playlist, adding song to queue, updating queue_embed, sending queue_embed and initializing song queue"""
    
        url = url1 + url2 + url3 + url4 + url5 + url6
        print(url)

        if not ctx.guild.voice_client in self.client.voice_clients:
            try:
                channel = ctx.author.voice.channel
                await channel.connect()
            except:
                await ctx.channel.send("You are not in a voice channel!")
                return
  
        if validators.url(url) != 1:
            url = Music_helpers.link(url)

        if validators.url(url) == 1 and 'list=' in url:
            playlist = Playlist(url)
            playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            for x in playlist.video_urls:
                try:
                    with YoutubeDL(self.YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(x, download = False)
                        video_title = info.get('title', None)
                        self.add_to_embed(video_title, x, info['duration'])
                    self.music_queue.append({"ctx": ctx, "song_url" : x, "FFMPEG_OPTIONS" : {'before_options': '-ss 00:00:00.00 -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}})
                    await asyncio.sleep(0.3)
                except Exception as e:
                    await ctx.channel.send(f"{e}")

        elif validators.url(url) == 1 and 'shorts' in url:
            url = Music_helpers.get_link_shorts(url)
            try:
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(url, download=False)
                        video_title = info.get('title', None)
                        self.add_to_embed(video_title, url, info['duration'])
                self.music_queue.append({"ctx": ctx, "song_url" : url, "FFMPEG_OPTIONS" : {'before_options': '-ss 00:00:00.00 -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}})
                await asyncio.sleep(0.2)
            except Exception as e:
                    await ctx.channel.send(f"{e}")
        else:
            try:
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(url, download=False)
                        video_title = info.get('title', None)
                        self.add_to_embed(video_title, url, info['duration'])
                self.music_queue.append({"ctx": ctx, "song_url" : url, "FFMPEG_OPTIONS" : {'before_options': '-ss 00:00:00.00 -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}})
                await asyncio.sleep(0.2)
            except Exception as e:
                    await ctx.channel.send(f"{e}")

        voice = get(self.client.voice_clients, guild=ctx.guild)
        if len(self.music_queue) > 1:
            if voice.is_playing() or voice.is_paused():
                await ctx.channel.send(embed=self.embed_queue, delete_after=8)
            else:
                await ctx.channel.send(embed=self.embed_queue, delete_after=8)
                if not voice.is_playing() and not voice.is_paused():
                  try:
                      await asyncio.sleep(0.2)
                      self.play_queue()
                  except Exception as e:
                      await ctx.channel.send(f"{e}")
        elif voice.is_playing() or voice.is_paused():
            await ctx.channel.send(embed=self.embed_queue, delete_after=8)
        else:
            if not voice.is_playing() and not voice.is_paused():
              try:
                  await asyncio.sleep(0.2)
                  self.play_queue()
              except Exception as e:
                  await ctx.channel.send(f"{e}")

                
def setup(client):
    client.add_cog(Playing_music(client))
