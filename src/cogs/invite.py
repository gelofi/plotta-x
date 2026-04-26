import discord
from discord import app_commands
from discord.ext import commands
link = 'https://discord.com/oauth2/authorize?client_id=1497873742502690867&permissions=5066826606570560&integration_type=0&scope=bot'

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='invite', description='Get an invite link for Plotta,')
    async def invite(self, interaction: discord.Interaction):
        invite = discord.Embed(
            title='Invite Plotta',
            description=f'Invite [Plotta]({link}) and use matplotlib in your server.',
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=invite)

async def setup(bot):
    await bot.add_cog(Invite(bot))
