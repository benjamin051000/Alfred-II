import discord
import asyncio
from discord.ext import commands
from discord.voice_client import VoiceClient
import sys, traceback
import configparser

print("Loading config data...\n")
configLoader = configparser.ConfigParser()
configLoader.read("..\\config.ini")


def configSectionMap(section):
    dict = {}
    options = configLoader.options(section)
    for option in options:
        try:
            dict[option] = configLoader.get(section, option)
            if dict[option] == -1:
                DebugPrint("skip: %s!" % option)
        except:
            print("exception on %s!" % option)
            dict[option] = None
    return dict

#######################    Begin Loading Process   ################################
startup_extensions = configSectionMap("Startup")["startup_extensions"].split()
command_prefix = configSectionMap("Commands")["command_prefix"]

bot = commands.Bot(command_prefix = commands.when_mentioned_or(command_prefix), description = configSectionMap("Startup")["description"])

print(bot.description)

#Load extensions
if __name__ == "__main__":
    print("\nLoading extensions...")
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print(f"Extension \'{extension}\' loaded.")
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():
    print("\nConnected to Discord as", bot.user.name, "- ID ", bot.user.id)
    print("Alfred II loaded successfully.\n______________________________\n")
    #await bot.change_presence(activity = discord.Activity(name = "", type = 2)) #type: 0-playing a game, 1-live on twitch, 2-listening, 3-watching

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user and message.content.startswith(command_prefix):
        return
    #hello
    if message.content.upper() in ("HELLO", "HI", "HEY", "GREETINGS", "SALUTATIONS", "YO"):
        await message.add_reaction("\U0001F44B") #waving hand

###################################################################################
bot.run(configSectionMap("Startup")["token"])
