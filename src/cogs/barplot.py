import discord, io
from discord import app_commands
import matplotlib.pyplot as plt
import numpy as np
from discord.ext import commands

class Bargraph(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='bargraph', description='Plot a bar graph using matplotlib.')
    @app_commands.describe(title='The title of this bar graph.')
    @app_commands.describe(description='Describe what this graph is for.')
    @app_commands.describe(names='X Axis: The entities we\'re comparing! Separated by [,] comma.')
    @app_commands.describe(values='Y Axis: The values of the entities we\'re comparing. Separated by [,] comma.')
    @app_commands.describe(grid='Adds a grid to the graph.')
    async def bargraph(self, interaction: discord.Interaction, title: str, description: str, names: str, values: str, grid: bool):
        try:
            plt.figure()
            x = np.array(list(names.replace(', ', ',').split(',')))
            y = np.array(list(map(float, values.replace(', ', ',').split(','))))
            plt.bar(x, y)
            plt.grid(grid)
            plt.title(title)
            # generate the bar graph as image
            with io.BytesIO() as image_binary:
                plt.savefig(image_binary, format='png')
                image_binary.seek(0)
                plt.close()
                # take the bar plot image and send it
                graph = discord.File(image_binary, filename='barplot.png')

                plot_embed = discord.Embed(
                    title=title,
                    description=description,
                    color=discord.Color.blue()
                )
                plot_embed.set_image(url='attachment://barplot.png')
                await interaction.response.send_message(embed=plot_embed, file=graph)
        except Exception as e:
            error_embed = discord.Embed(
                title='Error',
                description=e,
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            print("Error in making a bar graph. ", e)

async def setup(bot):
    await bot.add_cog(Bargraph(bot))