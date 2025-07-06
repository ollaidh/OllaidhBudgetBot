import discord
import os
import commands
import commands_handler
from db_adapters.firestore_adapter import FirestoreAdapter

intents = discord.Intents.all()
client = discord.Client(intents=intents)
adapter = FirestoreAdapter()
handler = commands_handler.CommandsHandler(adapter)

bot_token = os.getenv("DISCORD_BOT_TOKEN")
assert bot_token


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    try:
        print(f"Received message: {message.content}")
        msg_back = handler.handle_message(message.content)
        if not msg_back:
            return

        if "message" in msg_back:
            await message.channel.send(msg_back["message"])
        if "chart_path" in msg_back:
            msg_back["chart_path"].seek(0)
            file = discord.File(msg_back["chart_path"], "pie.png")
            await message.channel.send(file=file)
    except commands.BotException as err:
        msg_back = str(err)
        await message.channel.send(msg_back)


client.run(bot_token)
