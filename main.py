from bot_ping import ping_bot_endpoint
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

bot_url = os.getenv("BOT_URL")
assert bot_url

@client.event
async def on_connect() -> None:
    print(f"Bot connected")


@client.event
async def on_ready() -> None:
    print(f"We have logged in as {client.user=}")


@client.event
async def on_resumed() -> None:
    print(f"Resumed session as {client.user=}")


@client.event
async def on_disconnect() -> None:
    print(f"Bot disconnected")


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author == client.user:
        return

    try:
        print(f"Received message: {message.content}")
        msg_back = handler.handle_message(message.content)
        await ping_bot_endpoint(bot_url)  # ping bot to prevent it from falling asleep
        if not msg_back:
            return

        if "message" in msg_back:
            await message.channel.send(msg_back["message"])
        if "chart_path" in msg_back:
            msg_back["chart_path"].seek(0)
            file = discord.File(msg_back["chart_path"], "pie.png")
            await message.channel.send(file=file)
    except commands.BotException as err:
        await message.channel.send(str(err))


client.run(bot_token)
