import discord, io
from discord import app_commands
import matplotlib.pyplot as plt
import numpy as np
from discord.ext import commands

class Piechart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='piechart', description='Create a pie chart using matplotlib.')
    @app_commands.describe(title='The title of this bar graph.')
    @app_commands.describe(description='Describe what this graph is for.')
    @app_commands.describe(percentage='The value of each slice. Must sum up to a 100.')
    @app_commands.describe(labels='Label for each respective slice.')
    @app_commands.describe(colors='[Optional] Color for each respective slice. e.g. black, white, #FF0055')
    @app_commands.describe(shadow='[Optional] Adds a shadow effect to the pie.')
    @app_commands.describe(legend='[Optional] Adds a title for pie legend.')
    @app_commands.describe(show_percentage='Adds a percentage label to each slice.')
    async def piechart(self, interaction: discord.Interaction, title: str, description: str, percentage: str, labels: str, shadow: bool, show_percentage: bool, colors: str=None, legend: str=None):
        try:
            x = np.array(list(percentage.replace(', ', ',').split(',')))
            y = np.array(list(map(str, labels.replace(', ', ',').split(','))))
            show_pct = '%1.1f%%' if show_percentage else None
            colors_set = np.array(list(map(str, colors.replace(', ', ',').split(',')))) if colors is not None else None
            plt.pie(x, labels=y, startangle=90, autopct=show_pct, shadow=shadow, colors=colors_set)
            if legend is not None:
                plt.legend(title=legend)
                plt.axis('equal')
            plt.title(title)
            # generate the pie chart as image
            with io.BytesIO() as image_binary:
                plt.savefig(image_binary, format='png')
                image_binary.seek(0)
                plt.close()
                # take the pie chart image and send it
                graph = discord.File(image_binary, filename='piechart.png')

                plot_embed = discord.Embed(
                    title=title,
                    description=description,
                    color=discord.Color.blue()
                )
                plot_embed.set_image(url='attachment://piechart.png')
                await interaction.response.send_message(embed=plot_embed, file=graph)
        except Exception as e:
            error_embed = discord.Embed(
                title='Error',
                description=e,
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            print("Error in making a pie chart. ", e)

async def setup(bot):
    await bot.add_cog(Piechart(bot))