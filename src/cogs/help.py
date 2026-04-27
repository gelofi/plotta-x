import discord
from discord import app_commands
from discord.ext import commands
link = 'https://discord.com/oauth2/authorize?client_id=1497873742502690867&permissions=5066826606570560&integration_type=0&scope=bot'
github = 'https://github.com/gelofi/plotta'

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help', description='Gives a list of all the commands available.')
    async def help(self, interaction: discord.Interaction):
        help_embed = discord.Embed(
            title='Plotta v4.1',
            description=f'Thank you for using Plotta. You may visit the repository [here]({github}), or add Plotta to your server [here]({link}).',
            color=discord.Color.blue(),
        )
        for command in self.bot.tree.get_commands():
            help_embed.add_field(name=command.name, value=command.description, inline=False)

        await interaction.response.send_message(embed=help_embed)

async def setup(bot):
    await bot.add_cog(Help(bot))