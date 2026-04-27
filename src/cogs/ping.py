import discord
from discord import app_commands
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description='Returns the bot\'s latency.')
    async def ping(self, interaction: discord.Interaction):
        ping_embed = discord.Embed(
            title='Pong!',
            description=f'Plotta has a latency of {round(self.bot.latency * 1000)}ms.',
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=ping_embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))