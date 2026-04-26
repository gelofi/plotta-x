import discord
from discord.ext import tasks
from itertools import cycle

bot_statuses = cycle(["doing data cleaning...", "using matplotlib!!", "normalizing data..."])
@tasks.loop(seconds=180)
async def change_status(bot):
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))