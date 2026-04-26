import discord, io
from discord import app_commands
import matplotlib.pyplot as plt
from discord.ext import commands

class Plot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='plot', description='Plot a graph using matplotlib. Add intervals separated by [,] a comma.')
    async def plot(self, interaction: discord.Interaction, title: str, x_size: int, y_size: int, x_label: str, y_label: str, x_interval: str, y_interval: str, description: str):
        plt.figure(figsize=(x_size, y_size)) # create the plot
        x = [list(map(int, x_interval.split(",")))]
        y = [list(map(int, y_interval.split(",")))]
        plt.plot(x, y, marker='o', linestyle='-', color='blue') # plug in x and y axes
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        # generate the plot as an image
        with io.BytesIO() as image_binary:
            plt.savefig(image_binary, format='png')
            image_binary.seek(0)
            plt.close()
            # take the plot image and send it
            chart = discord.File(image_binary, filename='plot.png')

            plot_embed = discord.Embed(
                title=title,
                description=description,
                colour=discord.Colour.blue()
            )
            plot_embed.set_image(url='attachment://plot.png')

            await interaction.response.send_message(embed=plot_embed, file=chart)

async def setup(bot):
    await bot.add_cog(Plot(bot))