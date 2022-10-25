import nextcord
from nextcord.ext import commands
from os import listdir, environ

token = str(environ['token'])
bot_prefix = ","

intents = nextcord.Intents.all()
intents.members = intents.messages = intents.presences = True
client = commands.Bot(command_prefix=bot_prefix, intents=intents)
client.remove_command("help")

for filename in listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)
