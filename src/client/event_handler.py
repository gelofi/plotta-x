from client import status

async def load(bot):
    print(f'{bot.user.name} has connected to Discord!')
    status.change_status.start(bot)
    try:
        synced_commands = await bot.tree.sync()
        print(f'Upserted {len(synced_commands)} commands.')
    except Exception as e:
        print("An error with upserting commands has occurred. ", e)