import os

async def load(bot):
    for filename in os.listdir('src/cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename[:-3]} command')
        else:
            print(f'Skipped loading {filename}')