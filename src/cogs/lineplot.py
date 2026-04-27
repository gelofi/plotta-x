import discord, io
from typing import Literal
from discord import app_commands
import matplotlib.pyplot as plt
import numpy as np
from discord.ext import commands

class Lineplot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='lineplot', description='Plot a line graph using matplotlib. Add NUMERICAL intervals separated by [,] a comma.')
    @app_commands.describe(x_interval='X axis intervals. e.g. entry: 5,6,7,8,9')
    @app_commands.describe(y_interval='Y axis intervals. e.g. entry: 1,2,3,4,5')
    @app_commands.describe(title='The title of this plot.')
    @app_commands.describe(x_label='Describe the X axis.')
    @app_commands.describe(y_label='Describe the Y axis.')
    @app_commands.describe(description='Describe this plot for the embed.')
    @app_commands.describe(marker='The design of the dot on the plot.')
    @app_commands.describe(linestyle='The style of the plot line.')
    @app_commands.describe(color='The color of the plot line.')
    @app_commands.describe(grid='Adds a grid to the plot.')
    @app_commands.choices(marker=[
        app_commands.Choice(name='circle', value='o'),
        app_commands.Choice(name='scatter', value='s')
    ])
    async def lineplot(self, interaction: discord.Interaction, title: str,  description: str, x_label: str, y_label: str, x_interval: str, y_interval: str,marker: app_commands.Choice[str], linestyle: Literal['solid', 'dashed', 'dashdot', 'dotted'], color: Literal['red', 'orange', 'yellow', 'green', 'blue', 'purple'], grid: bool):
        try:
            x = np.array(list(map(float, x_interval.replace(', ', ',').split(","))))
            y = np.array(list(map(float, y_interval.replace(', ', ',').split(","))))
            plt.figure() # create the plot
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.grid(grid)
            plt.plot(x.squeeze(), y.squeeze(), marker=marker.value, linestyle=linestyle, color=color) # plug in x and y axes
            plt.title(title)
            # generate the plot as an image
            with io.BytesIO() as image_binary:
                plt.savefig(image_binary, format='png')
                image_binary.seek(0)
                plt.close()
                # take the line plot image and send it
                graph = discord.File(image_binary, filename='lineplot.png')

                plot_embed = discord.Embed(
                    title=title,
                    description=description,
                    color=discord.Color.blue()
                )
                plot_embed.set_image(url='attachment://lineplot.png')
                await interaction.response.send_message(embed=plot_embed, file=graph)
        except Exception as e:
            error_embed = discord.Embed(
                title='Error',
                description=e,
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            print("Error in making a line plot. ", e)

async def setup(bot):
    await bot.add_cog(Lineplot(bot))