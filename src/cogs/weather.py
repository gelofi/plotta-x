import discord
from discord import app_commands
from discord.ext import commands

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='weather', description='Returns the current weather conditions of a target location.')
    async def weather(self, interaction: discord.Interaction, message: str):
        weather_embed = discord.Embed(
            title=f'Weather Forecast at {message}',
            color=discord.Color.blue()
        )
        weather_embed.set_footer(text='Open-Meteo API <3')
        await interaction.response.send_message(embed=weather_embed)

async def setup(bot):
    await bot.add_cog(Weather(bot))