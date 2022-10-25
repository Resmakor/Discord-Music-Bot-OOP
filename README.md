# Discord Music Bot "Understandek" made with OOP

### Video Demo: https://youtu.be/ZxDVZb1gRaw
#
## Description
"Understandek" is a Discord Music Bot with many other features. At first (January 2022) Understandek was made for fun and due to the fact that most of the available music bots at that time were blocked from Discord. Bot was made in Python. In Oktober Understandek was refactorised: and written using OOP and ```nextcord``` API instead of ```discord.py```. Video demo was recorded before refactorization, however it shows Understandek's main capabilities.

#
# File "requirements.txt"
File "requirements.txt" is a list with the libraries needed for the bot to work.

**You have to install [FFmpeg](https://ffmpeg.org/) as well!**

#
# File "main.py"
File "main.py" is the crux of my project.
 At the beginning there is the initialization of the bot with environment variables, prefix to cause commands and some intents to make it all work.

```python 
token = str(environ['token'])
bot_prefix = ","

intents = nextcord.Intents.all()
intents.members = intents.messages = intents.presences = True
client = commands.Bot(command_prefix=bot_prefix, intents=intents)
```

Then ```cogs``` are being loaded:
```python 
for filename in listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
```
#
## File "music_helpers.py"
In file "music_helpers.py" there is one class called ```Music_helpers```. Functions inside of the following class are:
#
```python
def link(user_words):
```
- Function returns YouTube url for first video id found in HTML code from words typed by user.

To begin with, YouTube search engine works in such a way that the sum of the words you type in the search box is included in the constant: 
- ```https://www.youtube.com/results?search_query=<words from searchbox>```

![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/search_link_snippet.png?raw=true)

To make ```link``` more universal ```unidecode``` function removes non-ASCII characters (for instance German umlauts).

The next step is searching through HTML of the following page for video ids. We can distinct them due to the fact that each YouTube video url has a regular expression with 11 characters unique identifier. Thus we are looking for:
- ```watch\?v=<unique 11 characters>``` expression.

For that example final YouTube url returned by function ```link``` for user's words "dua lipa levitating" is:
-  ```https://www.youtube.com/watch?v=TUVcZfQe-Kw&ab_channel=DuaLipa```

**Be aware that sometimes the first search result in HTML code may not be what you are looking for! I decided to leave it as it is (first video id instead of user spending time choosing link), but it can be edited easily.**


#
```python
def get_colour(id):
```
- Function is responsible for finding the most suitable Discord embed colour. From the YouTube thumbnail the color palettes are separated and the middle one is always chosen.

![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/Embed.png?raw=true)
#
```python
def get_link_shorts(id):
```
- Function returns link to YouTube video, having received link to YouTube shorts.
#


# Cogs folder
Cogs folder is to organize a collection of commands and listeners. Each cog is a class that subclasses ```commands.Cog```.
#
## Cog ```Playing_music```
```python
def add_to_queue(self, url):
```
- Function adds song's url to ```list_of_songs``` (list of YouTube urls)
#
```python
def add_to_embed(self, video_title, url, duration):
```
- Function adds song to embed (```embed_queue```) related to queue.
#
```python
async def show_status(self, ctx, video_title, duration, id, colour_id):
```
- Function shows which song is being played and add reactions to some of them (beloved and disgusting list)
![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/bot_reaction_to_song.png?raw=true)
#
```python
def play_queue(self):
```
- Function plays music in ```list_of_songs``` order. When list of songs is empty, playing is finished.
#
```python
@commands.command()
    async def forward(self, ctx, seconds):
```
- Function rewinds the song by a given number of seconds. Support functions: ```show_time```, ```get_ss_time```.
#
```python
async def show_time(self, ctx, timer : str):
```
- Function shows time of a song already set.
#
```python
def get_ss_time(self, seconds, end):
```
- Function gets valid time (```FFMPEG``` type) after forward command in order to change ```FFMPEG OPTIONS```. For instance: "00:01:20.00".
![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/forward_command.png?raw=true)
#
```python
@commands.command()
    async def loop(self, ctx):
```
- Function starts loop by changing ```if_loop``` value. Loop makes it so that songs are no longer removed from the ```list_of_songs``` and ```ctx_queue```.
![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/loop_command.png?raw=true)
#
```python
@commands.command()
    async def queue(self, ctx):
```
- Function shows status of queue via sending ```embed_queue```.
![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/queue_embed.png?raw=true)
#
```python
@commands.command()
    async def play(self, ctx, url1 = "", url2 = "", url3 = "", url4 = "", url5 = "", url6 = ""):
```
Function ```play``` deals with:
- bot joining voice channel,
- getting valid YouTube url,
- downloading YouTube playlist/shorts,
- adding song to queue,
- updating queue_embed,
- sending queue_embed,
- initializing ```play_queue``` function.
Variables called ```url1```, ```url2```, ```url3```, ```url4```, ```url5```, ```url6``` are 6 words after command play. For instance, let's execute ```,play young leosia rok tygrysa```:
```python
url1 = "young", 
url2 = "leosia", 
url3 = "rok", 
url4 = "tygrysa", 
url5 = ""
url6 = ""
```
![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/play_command_whole.png?raw=true)

**I decided to do it this way so that the user would not enter too many words to search and for the sake of code readability**
#
## Cog ```Playing_music_helpers```
#
```python
 @commands.command()
    async def pause(self, ctx):
```
```python
@commands.command()
    async def resume(self, ctx):
```
```python
@commands.command()
    async def skip(self, ctx):
```
- These commands in order: ```pause```, ```resume```, ```skip``` the music.
![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/pause_resume_skip.png?raw=true)
#
```python
@commands.command()
    async def help(self, ctx):
```
- Function shows available commands with description.
#


## Cog ```Connecting```
#
```python
@commands.command()
    async def join(self, ctx)
```
- Bot joins voice channel.
#
```python
@commands.command()
    async def dc(self, ctx)
```
- Bot disconnects from voice channel and says goodbye via tts.
#

## Cog ```Messages```
#
```python
@commands.Cog.listener()
    async def on_ready(self):
```
- Function changes bot Discord status, when bot is online.
#
```python
@commands.Cog.listener()
    async def on_message(self, message):
```
- Bot responds to keywords related to 'xD' emote.

#
## Cog ```Accesories```
```python
@commands.command()
    async def listen(self, ctx, member : nextcord.Member):
```
- Function send messages with some details about discord member who's listening to song on Spotify. Embed is not impressive, that command was fully made for fun.
![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/listen_command.PNG?raw=true)

#
```python
@commands.command()
    async def clear(self, ctx, amount):
```
- Bot clears text channel by deleting its own messages and messages with bot prefix.
- Bot searches through amount of messages behind. 
![alt text](https://github.com/Resmakor/Discord-Music-Bot/blob/main/snippets/clear_command.png?raw=true)
#
```python
@commands.command()
    async def coin(self, ctx):
```
- Bot tosses a coin.
#
```python
@commands.command()
    async def cannon(self, ctx, member : nextcord.Member):
```
- Bot is moving specific user through all channels. Afterwards user is back on his previous voice channel. You can see how it works in demo on YouTube. You have to own "cannon" role on the server.
#
