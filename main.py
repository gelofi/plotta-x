import asyncio, os, discord
from discord.ext import commands
from dotenv import load_dotenv

# utilities
from client import command_handler, event_handler

load_dotenv() # load variables from .env into the system environment
token = os.getenv("TOKEN") # the token in the .env file

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    await event_handler.load(bot)  # event handler

# main method
async def main():
    async with bot:
        await command_handler.load(bot) # command handler
        await bot.start(token)

asyncio.run(main())