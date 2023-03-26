import discord
import os
import commands
import commands_handler
from db_adapters.firestore_adapter import FirestoreAdapter

intents = discord.Intents.all()
client = discord.Client(intents=intents)
adapter = FirestoreAdapter()
handler = commands_handler.CommandsHandler(adapter)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    try:
        msg_back = handler.handle_message(message.content)
        if 'message' in msg_back:
            await message.channel.send(msg_back['message'])
        elif 'chart_path' in msg_back:
            await message.channel.send(file=discord.File(msg_back['chart_path']))
    except commands.BotException as err:
        msg_back = str(err)
        await message.channel.send(msg_back)


client.run(os.getenv('DISCORD_BOT_TOKEN'))

