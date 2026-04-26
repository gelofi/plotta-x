import discord
from discord import app_commands
from discord.ext import commands
import requests

# weather information fetcher
async def weather(city: str):
    try:
        res = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city}')
        data = res.json()
        if res.status_code == 200:
            place = data['results'][0]['name']
            country = data['results'][0]['country']
            lat = data['results'][0]['latitude']
            lon = data['results'][0]['longitude']
            try:
                weather_res = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=relative_humidity_2m,temperature_2m,precipitation,rain,wind_speed_10m,showers,apparent_temperature,weather_code,surface_pressure')
                weather_data = weather_res.json()
                if weather_res.status_code == 200:
                    temperature = f"{weather_data['current']['temperature_2m']}{weather_data['current_units']['temperature_2m']}"
                    humidity = f"{weather_data['current']['relative_humidity_2m']}{weather_data['current_units']['relative_humidity_2m']}"
                    wind_speed = f"{weather_data['current']['wind_speed_10m']} {weather_data['current_units']['wind_speed_10m']}"
                    surface_pressure = f"{weather_data['current']['surface_pressure']} {weather_data['current_units']['surface_pressure']}"
                    return country, place, temperature, humidity, wind_speed, surface_pressure
            except Exception as e:
                print("An error occurred while fetching for weather information.", e)
                return None, None, None, None, None, None
    except Exception as e:
        print("An error occurred while fetching for the location.", e)
        return None, None, None, None, None, None

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='weather', description='Returns the current weather conditions of a target location.')
    async def weather(self, interaction: discord.Interaction, location: str):
        country, place, temperature, humidity, wind_speed, surface_pressure = await weather(location)
        if country is not None:
            weather_embed = discord.Embed(
                title=f'Weather Forecast at {place}, {country}',
                color=discord.Color.blue()
            )
            weather_embed.add_field(name='Temperature', value=temperature, inline=False)
            weather_embed.add_field(name='Humidity', value=humidity, inline=False)
            weather_embed.add_field(name='Wind speed', value=wind_speed, inline=False)
            weather_embed.add_field(name='Surface pressure', value=surface_pressure, inline=False)
            weather_embed.set_footer(text='Uses Open-Meteo API <3')
            await interaction.response.send_message(embed=weather_embed)
        else :
            error_embed = discord.Embed(
                title='Error',
                description=f'An error occurred while fetching for the location.',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
async def setup(bot):
    await bot.add_cog(Weather(bot))